import re
import time
import sys
import json
from Adafruit_IO import MQTTClient
from Backend.test import Gauss, KNN

AIO_FEED_ID = "homeinfo"
AIO_USERNAME = "baokhanhle123"
AIO_KEY = "aio_AlTH51bsR3JWjNtaAYfVpefBRasj"


def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe(AIO_FEED_ID)


def subscribe(client, userdata, mid, granted_qos):
    print("Subcribe thanh cong ... ")


def disconnected(client):
    print("Ngat ket noi ... ")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Nhan du lieu : " + payload)
    temp = payload[9:11]
    humi = payload[25:27]
    predict(temp, humi)

def predict(temp, humi):
    print(temp)
    print(humi)
    classifiled = Gauss(temp, humi)
    result = ""
    if classifiled == "class1": result = "Trời không mưa"
    if classifiled == "class2": result = "Trời có thể mưa nhỏ"
    if classifiled == "class3": result = "Trời có mưa nhỏ"
    if classifiled == "class4": result = "Trời có mưa vừa"
    if classifiled == "class5": result = "Trời mưa to"
    time.sleep(10)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    print('Get the last record')
    data = client.receive('homeinfo')
    time.sleep(10)
