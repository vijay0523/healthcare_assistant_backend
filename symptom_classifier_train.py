import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tensorflow as tf
import random
import json
import pickle

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
from keras import regularizers
import random
import shap
import numpy as np

tf.compat.v1.disable_v2_behavior()

with open("symptom_intents.json") as file:
    data = json.load(file)


words = []
labels = []
docs_x = []
docs_y = []

#tokenizing each pattern in our dataset
#adding to list of tokenize patterns or wrds and their labels or tag
# for intent in data["intents"]:
#     for pattern in intent["patterns"]:
#         wrds = nltk.word_tokenize(pattern)
#         words.extend(wrds)
#         docs_x.append(wrds)
#         docs_y.append(intent["tag"])

#     if intent["tag"] not in labels:
#         labels.append(intent["tag"])

# text_symptoms = []
# labels_symptoms = []
for c in data["intents"]:
    wrds = nltk.word_tokenize(c[2])
    words.extend(wrds)
    docs_x.append(wrds)
    docs_y.append(c[0])
    if c[0] not in labels:
        labels.append(c[0])

#reducing each words to their root word and sorting them
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

#inserting list of words and labels into pickle file 
#performing serialization
pickle.dump(words,open('words1.pkl','wb'))
pickle.dump(labels,open('labels1.pkl','wb'))



training = []
output = []

out_empty = [0 for _ in range(len(labels))]

#encoding our input to bag of words
for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

#creating bag of words encoding of dataset
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


# if load_model('chatbot_model.h5'):
#     print('Model Loaded')
#     model = load_model('chatbot_model.h5')
#     background = training[np.random.choice(training.shape[0], 100, replace=False)]
#     shap.explainers._deep.deep_tf.op_handlers["AddV2"] = shap.explainers._deep.deep_tf.passthrough

# #     # explain predictions of the model on images
#     explainer = shap.DeepExplainer(model, background)
#     shap_values = explainer.shap_values(training)
#     # plot SHAP values
#     # plot_actual_predicted(images_dict, predicted_class)
#     print()
#     shap.image_plot(shap_values, training * 255)
#     # print(e)
#     exit(0)

#building deep neural networks
model = Sequential()
model.add(Dense(248, input_shape=(len(training[0]),), activation='relu', kernel_regularizer=regularizers.l2(0.01)))
# model.add(Dropout(0.01))
model.add(Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
# model.add(Dropout(0.01))
model.add(Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
# model.add(Dropout(0.01))
model.add(Dense(len(output[0]), activation='softmax'))


# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.05, decay=1e-3, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


#fitting and saving the model 
hist = model.fit(np.array(training), np.array(output), epochs=1000, batch_size=30, verbose=1)
model.save('symptom_classifier_model.h5', hist)



