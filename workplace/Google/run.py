# import flask dependencies
from flask import Flask, request, make_response, jsonify
import shutil
import subprocess
import json
from function import question_processing,tokenize_and_filter,tokenizer
import pandas as pd
import numpy as np
import tensorflow as tf
from konlpy.tag import Kkma
from konlpy.utils import pprint
kkma = Kkma()
# initialize the flask app
keras = tf.keras
app = Flask(__name__)

intentdf = pd.read_csv('train_intent.csv',encoding="CP949")
entitydf = pd.read_csv('Entitytest.csv',encoding = "CP949")

intenttoken = tokenizer()
intenttoken.fit(intentdf['question'].values)

entitytoken = tokenizer()
entitytoken.fit(entitydf['word'].values)

intentmodel = keras.models.load_model('my_model.h5')
entitymodel = keras.models.load_model('entitytestmodel.h5')

def 형태소분석(text):
    형태소 = kkma.pos(text)
    명사 = []
    for i in 형태소:
        if i[1] == 'NNG':
            명사.append(i[0])
        else:
            pass
    return 명사

def entity분석(명사):
    inputdata = question_processing(명사,entitytoken)
    prediction = list(np.argmax(entitymodel.predict(inputdata),axis=1))
    print(명사)
    print(prediction)
    result = {}
    for a,b in zip(명사,prediction):
        if b == 0:
            result[a] = 'color'
        elif b == 1:
            result[a] = 'thing'
        elif b == 2:
            result[a] = 'loc'
    return result  

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json()
    print(req)
    intent = req['queryResult']['intent']['displayName']
    text = req['queryResult']['queryText']
    print("유저가 한 말 : "+text)
    inputdata = question_processing([text],intenttoken)
    prediction = np.argmax(intentmodel.predict(inputdata),axis=1)
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
    elif intent == 'pick':
        noun = 형태소분석(text)
        result = entity분석(noun)
        key = result.keys()
        returntext = ''
        for i in key:
            returntext += (i+' = '+result[i]+' ')
        return {'fulfillmentText':returntext}
    else:
        return {'fulfillmentText':'죄송합니다 잘 알아듣지 못했어요'}

    # print(req)    
    

    # return {'fulfillmentText': "파일이동완료"} #3



# run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0',port =80)

#%%
명사 = ['노란색','위','테이블']
inputdata = question_processing(명사,token)
prediction = list(np.argmax(entitymodel.predict(inputdata),axis=1))


# %%
print(prediction)