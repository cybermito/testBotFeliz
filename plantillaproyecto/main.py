from mltext import classifyText, storeText
from mlmodel import trainModel, checkModel



API_KEY = "CHANGE THIS TO YOUR PROJECT API KEY"


# -------------------------------------------------------
# CHECK IF THE MACHINE LEARNING MODEL IS READY TO USE
# -------------------------------------------------------

# you can use this to check if your machine learning model
# has finished training 

status = checkModel(API_KEY)
print (status)




# -------------------------------------------------------
# USE YOUR MACHINE LEARNING MODEL TO RECOGNIZE TEXT 
# -------------------------------------------------------

# CHANGE THIS to the text that you want your 
# machine learning model to classify
test_text = "The text that you want to test"

demo = classifyText(API_KEY, test_text)

label = demo["class_name"]
confidence = demo["confidence"]

# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))




# -------------------------------------------------------
# ADD TRAINING EXAMPLES TO YOUR MACHINE LEARNING PROJECT
# -------------------------------------------------------

# CHANGE THIS to the text that you want to add 
# to your project training data
training_text = "Training Example From Python"

# CHANGE THIS to the training bucket to add the
# training example to
training_label = "Label"

# remove the comment on the next line to use this 
# storeText(API_KEY, training_text, training_label)




# -------------------------------------------------------
# TRAIN A NEW MACHINE LEARNING MODEL
# -------------------------------------------------------

# after collecting new training examples, you can use 
# to train a new machine learning model 

# remove the comment on the next line to use this 
# trainModel(API_KEY)
