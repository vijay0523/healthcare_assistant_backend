from flask import Flask, request, jsonify
import requests
from web3 import Web3
import os
from flask_cors import CORS, cross_origin

import nltk
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import json
import random

import pickle
import numpy as np
from keras.models import load_model, save_model

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def home():
    # return "Hello, World!"
    return "Hello, World!"

model = load_model('chatbot_model.h5')
intents = json.loads(open('intents2.json').read())
intents3 = json.loads(open('intents3.json').read())
intents_symptoms = json.loads(open('symptom_intents.json').read())
commands = np.array(intents3['intents'])
commands = commands.T
commands1 = np.array(intents_symptoms['intents'], dtype=object)
# commands1 = commands1.T
# commands1 = commands1.T
# commands1 = commands1.T
# print(commands1[0][0])
text3 = commands[0]
labels3 = commands[1]
labels3_text = ["schedule_appointment", "who_made_you", "greeting", "goodbye", "invalid"]
# text_symptoms = commands1[2]
# labels_symptoms = commands1[1]]
text_symptoms = []
labels_symptoms = []
for c in commands1:
    text_symptoms.append(c[2])
    labels_symptoms.append(c[1])
# labels_symptoms = []
# print(text_symptoms)
labels_symptoms_text = ['hypertensive  disease',
'diabetes',
'depression  mental',
'depressive disorder',
'coronary  arteriosclerosis',
'coronary heart disease',
'pneumonia',
'failure  heart congestive',
'accident  cerebrovascular',
'asthma',
'myocardial  infarction',
'hypercholesterolemia',
'infection',
'infection  urinary tract',
'anemia',
'chronic  obstructive airway disease',
'dementia',
'insufficiency  renal',
'confusion',
'degenerative  polyarthritis',
'hypothyroidism',
'anxiety  state',
'malignant  neoplasms',
'primary malignant neoplasm',
'acquired  immuno-deficiency  syndrome',
'HIV',
'hiv infections',
'cellulitis',
'gastroesophageal  reflux disease',
'septicemia',
'systemic  infection',
'sepsis (invertebrate)',
'deep  vein thrombosis',
'dehydration',
'neoplasm',
'embolism  pulmonary',
'epilepsy',
'cardiomyopathy',
'chronic  kidney failure',
'carcinoma',
'hepatitis  C',
'peripheral  vascular disease',
'psychotic  disorder',
'hyperlipidemia',
'bipolar  disorder',
'obesity',
'ischemia',
'cirrhosis',
'exanthema',
'benign  prostatic hypertrophy',
'kidney  failure acute',
'mitral  valve insufficiency',
'arthritis',
'bronchitis',
'hemiparesis',
'osteoporosis',
'transient  ischemic attack',
'adenocarcinoma',
'paranoia',
'pancreatitis',
'incontinence',
'paroxysmal  dyspnea',
'hernia',
'malignant  neoplasm of prostate',
'carcinoma prostate',
'edema  pulmonary',
'lymphatic  diseases',
'stenosis  aortic valve',
'malignant  neoplasm of breast',
'carcinoma breast',
'schizophrenia',
'diverticulitis',
'overload  fluid',
'ulcer  peptic',
'osteomyelitis',
'gastritis',
'bacteremia',
'failure  kidney',
'sickle  cell anemia',
'failure  heart',
'upper  respiratory infection',
'hepatitis',
'hypertension  pulmonary',
'deglutition  disorder',
'gout',
'thrombocytopaenia',
'hypoglycemia',
'pneumonia  aspiration',
'colitis',
'diverticulosis',
'suicide  attempt',
'Pneumocystis  carinii pneumonia',
'hepatitis  B',
'parkinson  disease',
'lymphoma',
'hyperglycemia',
'encephalopathy',
'tricuspid  valve insufficiency',
"Alzheimer's  disease",
'candidiasis',
'oral  candidiasis',
'neuropathy',
'kidney  disease',
'fibroid  tumor',
'glaucoma',
'neoplasm  metastasis',
'malignant  tumor of colon',
'carcinoma colon',
'ketoacidosis  diabetic',
'tonic-clonic  epilepsy',
'tonic-clonic seizures',
'respiratory  failure',
'melanoma',
'gastroenteritis',
'malignant  neoplasm of lung',
'carcinoma of lung',
'manic  disorder',
'personality  disorder',
'primary  carcinoma of the liver cells',
'emphysema  pulmonary',
'hemorrhoids',
'spasm  bronchial',
'aphasia',
'obesity  morbid',
'pyelonephritis',
'endocarditis',
'effusion  pericardial',
'pericardial effusion body substance',
'chronic  alcoholic intoxication',
'pneumothorax',
'delirium',
'neutropenia',
'hyperbilirubinemia',
'influenza',
'dependence',
'thrombus',
'cholecystitis',
'hernia  hiatal',
'migraine  disorders',
'pancytopenia',
'cholelithiasis',
'biliary  calculus',
'tachycardia  sinus',
'ileus',
'adhesion',
'delusion',
'affect  labile',
'decubitus  ulcer']
# print(text_symptoms)
# print(labels_symptoms)
# exit()
words = pickle.load(open('words.pkl','rb'))
labels = pickle.load(open('labels.pkl','rb'))

@app.route("/chat", methods=['POST'])
def chatbot_response():
    print(request.json)
    print(request.json['msg'])
    print(request.form.get('msg'))
    msg = request.json['msg']
    # ints = predict_class(msg, model)
    # res = getResponse(ints, intents)
    res = dict()
    intent, pred = model_predict_intent(msg, "model.h5", text3, labels3_text)
    res['reply'] = pred
    res['intent'] = intent

    # res = model_predict(msg)
    # res = "Hello"
    return jsonify(res)

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": labels[r[0]], "probability": str(r[1])})
    print(return_list)
    return return_list

#getting chatbot response
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding, Flatten
from keras.models import Model
from keras.models import Sequential
from keras.initializers import Constant
MAX_SEQUENCE_LENGTH = 10
MAX_NUM_WORDS = 5000

def train_model(text, labels, labels_text, model_name):
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(text)
    sequences = tokenizer.texts_to_sequences(text)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    labels = to_categorical(np.asarray(labels))
    print('Shape of data tensor:', data.shape)
    print('Shape of label tensor:', labels.shape)
    VALIDATION_SPLIT = 0.1
    indices = np.arange(data.shape[0])
    np.random.shuffle(indices)
    data = data[indices]
    labels = labels[indices]
    num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])
    x_train = data[:-num_validation_samples]
    y_train = labels[:-num_validation_samples]
    x_val = data[-num_validation_samples:]
    y_val = labels[-num_validation_samples:]
    EMBEDDING_DIM = 60
    num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
    embedding_layer = Embedding(num_words,EMBEDDING_DIM,input_length=MAX_SEQUENCE_LENGTH,trainable=True)
    sequence_input = Input(shape=(MAX_SEQUENCE_LENGTH,), dtype='int32')
    embedded_sequences = embedding_layer(sequence_input)
    x = Conv1D(64, 3, activation='relu')(embedded_sequences)
    x = Conv1D(64, 3, activation='relu')(x)
    x = MaxPooling1D(2)(x)
    x=Flatten()(x)
    x = Dense(100, activation='relu')(x)
    preds = Dense(len(labels_text), activation='softmax')(x)
    model = Model(sequence_input, preds)
    model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['acc'])
    model.summary()
    s=0.0
    for i in range (1,15):
        model.fit(x_train, y_train,batch_size=50, epochs=30, validation_data=(x_val, y_val))
        # evaluate the model
        scores = model.evaluate(x_val, y_val, verbose=0)
        s=s+(scores[1]*100)
        # break

    # evaluate the model
    scores = model.evaluate(x_val, y_val, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    data = pad_sequences(tokenizer.texts_to_sequences(["Im sufering shortness  of breath, dizziness and chest pain"]), maxlen=MAX_SEQUENCE_LENGTH)
    # make a prediction
    yprob = model.predict(data)
    print(yprob)
    for prob in yprob:
        # print(prob)
        print(np.argmax(prob))
        print(labels_text[np.argmax(prob)])
        break
    model.save(model_name)
    exit()

def model_predict_intent(sentence, model_name, text, labels_text):
    # sentence = "hi"
    model = load_model(model_name)
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(text)
    data = pad_sequences(tokenizer.texts_to_sequences([sentence]), maxlen=MAX_SEQUENCE_LENGTH)
    # make a prediction
    yprob = model.predict(data)
    print(yprob)
    prediction = ""
    intent = ""
    for prob in yprob:
        # print(prob)
        print(np.argmax(prob))
        print(labels_text[np.argmax(prob)])
        intent = labels_text[np.argmax(prob)]
        break
    if(np.argmax(yprob[0])==0):
        answers = ["Sure! I can do that", "Sure! When do you want me to schedule the appointment?", "Sure! Can i know what time you are available?"]
        prediction = random.choice(answers)
    if(np.argmax(yprob[0])==2):
        answers = ["Hello there!", "Hi, What can i do for you today?", "Hey there! How can i help you?", "Hi!"]
        prediction = random.choice(answers)
    if(np.argmax(yprob[0])==4):
        answers = ["Sorry, I could not understand what you meant..! Could you repeat?", "Sorry, I cannot do that!", "Sorry! My skills are currently limited", "Sorry i cannot do that right not!", "Sorry, I cannot understand that!"]
        prediction = random.choice(answers)
    
    return intent, prediction

def model_predict_symptom(sentence, model_name, text, labels_text):
    # sentence = "hi"
    model = load_model(model_name)
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(text)
    data = pad_sequences(tokenizer.texts_to_sequences([sentence]), maxlen=MAX_SEQUENCE_LENGTH)
    # make a prediction
    yprob = model.predict(data)
    print(yprob)
    prediction = ""
    intent = ""
    for prob in yprob:
        # print(prob)
        print(np.argmax(prob))
        print(labels_text[np.argmax(prob)])
        intent = labels_text[np.argmax(prob)]
        break
    if(np.argmax(yprob[0])==0):
        answers = ["Sure! I can do that", "Sure! When do you want me to schedule the appointment?", "Sure! Can i know what time you are available?"]
        prediction = random.choice(answers)
    if(np.argmax(yprob[0])==2):
        answers = ["Hello there!", "Hi, What can i do for you today?", "Hey there! How can i help you?", "Hi!"]
        prediction = random.choice(answers)
    if(np.argmax(yprob[0])==4):
        answers = ["Sorry, I could not understand what you meant..! Could you repeat?", "Sorry, I cannot do that!", "Sorry! My skills are currently limited", "Sorry i cannot do that right not!", "Sorry, I cannot understand that!"]
        prediction = random.choice(answers)
    
    return intent, prediction

# train_model(text3, labels3, labels3_text, "model.h5")
train_model(text_symptoms, labels_symptoms, labels_symptoms_text, "model_symptoms.h5")
# model_predict_intent("hi", "model.h5", text3, labels3_text)
# model_predict_symptom("Im sufering shortness  of breath, dizziness and chest pain", "model_symptoms.h5", text_symptoms, labels_symptoms_text)
    
if __name__ == "__main__":
    app.run(debug=True)