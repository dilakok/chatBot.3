import encodings
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
import uvicorn
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from tensorflow.python.framework import ops
ops.reset_default_graph()
import requests
import numpy
import tflearn
import tensorflow as tf
import random
import json
import pickle
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create flask object
# encoding:utf-8
#!/usr/bin/env python
#-*-coding:utf-8-*-
app = FastAPI()
      
tf.compat.v1.reset_default_graph()
with open("intents.json") as file:
    data = json.load(file) 

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

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

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
    
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")
headers = {

"user-agent": "ravenfo",
'Content-Type': 'application/json'

}

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

class Data(BaseModel):
    inp: str


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  


@app.post('/check')
async def check(request: Request):
    da = await request.form()

    soru = "nasılsın"

    data2 = jsonable_encoder(da)
    soru = data2['param1']

    #while True:

    results = model.predict([bag_of_words(soru, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.7:
    
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        return  random.choices(responses)[0]  
    else:
        return "ne dedigini anlayamadım, tekrar dener misin?"

    #da = jsonable_encoder(da)
    #print(da)
    return da     

@app.get('/info')
def chat(data: Data):
   # return data
    print("Merhaba ben  QBot, nasıl yardımcı olabilirim!")

    results = model.predict([bag_of_words(data.inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    if results[results_index] > 0.7:
        for tg in data["intents"]:  
            if tg['tag'] == tag:
                responses = tg['responses']
        return {'msg: ',random.choices(responses)[0], encodings =='utf8'} 
    else:
     return {'msg: ':'ne dedigini anlayamadım, tekrar dener misin?'}      
                
if __name__ == "__main__":
     uvicorn.run(app, port = 7201, debug=True)  