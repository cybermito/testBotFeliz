import logging

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests
from PIL import Image
from constantes import API_KEY, CYBERMITOTOKEN
#creamos el registro de (logs) para tener información de cualquier error que ocurra en el proceso
#de conexión con la API de Telegram
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

AGREGAR = range(0)

#Creamos los objetos updater y dispatcher para la comunicación con el Bot.
updater = Updater(token=CYBERMITOTOKEN, use_context=True)
dispatcher = updater.dispatcher

#Definimos las funciones para los comandos de inicio, fin y ayuda.
#responderán a los comandos /start, /adios, /help.
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola, soy un bot, por favor habla conmigo")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /help para obtener ayuda en el funcionamiento")
    siEntrenado = checkModel(API_KEY)

    if siEntrenado['status'] == 'ready to use':
        context.bot.send_message(chat_id=update.effective_chat.id, text="¿Que quieres decirme?")

    else:
        #context.bot.send_message(chat_id=update.effective_chat.id, text=siEntrenado)
        trainModel(API_KEY)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Estoy volviendo a generar el modelo de entrenamiento...")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Espera unos segundos y vuelve a escribir /start para comenzar.")


def help(update: Update, context: CallbackContext):
    mensaje="Este bot responde a las emociones que le crean las palabras o frases que se le diga"
    mensaje2="Si le dices cosas que no le gustan, se pondrá triste y si, sí le gustan, se pondra alegre"
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje2)

def adios(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Que pena que te vayas. Voy a desconectarme")
    updater.stop()

#En esta función recibiremos el mensaje del usuario, el cuál pasaremos a ML4K
def mensajeRecibido(update: Update, context: CallbackContext):
    texto = update.message.text
    reply_keyboard = [['Si', 'No']]
    recognized = classify(texto)

    #Aquí compruebo si he recibido alguna clasificación, si es así ejecuto la condición. 
    if recognized != None:
        label = recognized['class_name']

        if label == "cosas_buenas":
            context.bot.send_message(chat_id=update.effective_chat.id, text="Muchas gracias, eres muy agradable")
            with open('img/feliz.jpg', 'rb') as imagen:
                context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=imagen)
                
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No me ha gustado lo que has dicho")
            with open('img/triste.jpg', 'rb') as imagen:
                context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=imagen)
        
    else:
        print(update.message.reply_text(
            'No entendi lo que me digiste'
            '¿Quieres agregar el texto a la lista de aprendizaje? (Si/no)',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Si o No?'
            ),
        ))
        print(AGREGAR)
        return AGREGAR



# This function will pass your text to the machine learning model
# and return the top result with the highest confidence.
def storeText(key, text, label):
  #checkApiKey(key)
    
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/train")

  response = requests.post(url, 
                           json={ "data" : text, "label" : label })

  if response.ok == False:
    # if something went wrong, display the error
    print (response.json())

#Esta función ejecuta la creación de un nuevo modelo de entrenamiento con las palabras nuevas que
#hemos agregado.

def trainModel(key):
  #checkApiKey(key)
  
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/models")

  response = requests.post(url)

  if response.ok == False:
    # if something went wrong, display the error
    print (response.json())


def checkModel(key):
  #checkApiKey(key)
  
  url = ("https://machinelearningforkids.co.uk/api/scratch/" + 
         key + 
         "/status")

  response = requests.get(url)

  if response.ok:
    responseData = response.json()

    status = {
      2 : "ready to use",
      1 : "training is in progress",
      0 : "problem"
    }

    return { 
      "status" : status[responseData["status"]], 
      "msg" : responseData["msg"] 
    }
  else:
    # if something went wrong, display the error
    print (response.json())


def ingresarNuevoEjemplo(text):
    
    respuestaUsuario = input("¿Quiere añadir la palabra al modelo de entrenamiento? (S/N) ")
    respuestaUsuario = respuestaUsuario.lower()

    if respuestaUsuario == 's':
        print()
        print("Vamos a añadir un nuevo texto, el texto va a ser: ", text)

        etiqueta = input("¿Dónde quieres añadir el ejemplo? (cosas_buenas o cosas_malas)")
        etiqueta = etiqueta.lower()

        if etiqueta == 'cosas_buenas':
            print()
            print("Vamos a añadir", text, "a la etiqueta", etiqueta)
            storeText(API_KEY, text, etiqueta)
            print("Entrenando...")
            trainModel(API_KEY)
            print("Ya está añadida el nuevo texto y entrenado.")

        
        elif etiqueta == 'cosas_malas':
            print()
            print("Vamos a añadir", text, "a la etiqueta", etiqueta)
            storeText(API_KEY, text, etiqueta)
            print("Entrenando...")
            trainModel(API_KEY)
            print("Ya está añadido el nuevo texto y entrenado.")

        else:
            print("La respuesta tiene que ser cosas_buenas o cosas_malas, una de las dos opciones")



    elif respuestaUsuario == 'n':
        print("Has respondido NO")
    
    else:
        print("Tienes que responder con S para Si o con N para No")



def classify(text):
    key = API_KEY
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"
    
    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        confidence = responseData[0]

        #print(responseData)
        #print()
        
        if confidence['confidence'] >= 60:
            topMatch = responseData[0]
            return topMatch

        else:
            #print("No entiendo la respuesta")
            #ingresarNuevoEjemplo(text)
            return None

    else:
        response.raise_for_status()

# Cambiamos a partir de aquí la forma de usar el módelo de entrenamiento. 
#demo = classify("Eres bonito")

#label = demo["class_name"]
#confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
#print ("result: '%s' with %d%% confidence" % (label, confidence))

def run():

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    adios_handler = CommandHandler('adios', adios)
    dispatcher.add_handler(adios_handler)

    mensajeRecibido_handler = MessageHandler(Filters.text & (~Filters.command), mensajeRecibido)
    dispatcher.add_handler(mensajeRecibido_handler)
        

    updater.start_polling()
    updater.idle()
    

if __name__ == '__main__':
    run()

   