# import flask dependencies
from flask import Flask, request, make_response, jsonify
import shutil
import subprocess
import json
from function import question_processing,tokenize_and_filter,tokenizer
import pandas as pd
import numpy as np
import tensorflow as tf
# initialize the flask app
keras = tf.keras
app = Flask(__name__)

df = pd.read_csv('train_intent.csv',encoding="CP949")
token = tokenizer()
token.fit(df['question'].values)
tempmodel = keras.models.load_model('my_model.h5')

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')

    # return a fulfillment response
    return {'fulfillmentText': 'This is a response from webhook.'}

# create a route for webhook
# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json()
    print(req)
    intent = req['queryResult']['intent']['displayName']
    text = req['queryResult']['queryText']
    print("유저가 한 말 : "+text)
    inputdata = question_processing([text],token)
    prediction = np.argmax(tempmodel.predict(inputdata),axis=1)
    print("예측 값 : {}".format(prediction[0]))
    if intent == 'Internet' and prediction[0] == 0:
        path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        subprocess.call(path)
        print("internet done")
        return {'fulfillmentText':'인터넷을 켰어요'}
    elif intent == 'Paint' and prediction[0] == 1:
        path = "C:\WINDOWS\system32\mspaint.exe"
        subprocess.call(path)
        print("paint done")
        return {'fulfillmentText':'그림판을 켰어요'}
    else:
        return {'fulfillmentText':'죄송합니다 잘 알아듣지 못했어요'}

    # print(req)    
    

    # return {'fulfillmentText': "파일이동완료"} #3



# run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0',port =80)