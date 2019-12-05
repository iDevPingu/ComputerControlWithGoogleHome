from flask import Flask,request,jsonify
import sys
import requests
import json
import urllib.request
def NaverSTT_API(filename):
    client_id = "6o5vqlnxzu"
    client_secret = "dkpdUZCoI1suTDn3e5HeOp0Dh5SMdWQm9r7R0zXz"
    url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang="+"Kor"

    # headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = open("{}".format(filename),'rb')
    # params = {"lang" : "Kor"}
    headers = {"X-NCP-APIGW-API-KEY-ID" : client_id,
                "X-NCP-APIGW-API-KEY" : client_secret,
                "Content-Type" : "application/octet-stream"}

    response = requests.post(url, data=data ,  headers = headers)
    print(response)
    print(response.text)
    return 0 

def NaverTTS_API():
    client_id = "6o5vqlnxzu"
    client_secret = "dkpdUZCoI1suTDn3e5HeOp0Dh5SMdWQm9r7R0zXz"
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    encText = urllib.parse.quote("반갑습니다 네이버")
    data = "speaker=mijin&speed=0&text=" + encText
    
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('1111.mp3', 'wb') as f:
            f.write(response_body)
        NaverSTT_API('1111.mp3')
    else:
        print("Error Code:" + rescode)

# @app.route('/hello',methods = ['GET','POST'])
# def Hello():
#     message = {
#         "client_id":"",
#         "device_id":"",
#         "model_id":"",
#         "response_type":"code",
#         "state":""
#     }
#     return jsonify(message)

if __name__ == "__main__":
    NaverTTS_API()