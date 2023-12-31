from kafka import KafkaConsumer
import json
import pprint
import threading
import time
import datetime
from pymongo import MongoClient

client = MongoClient('docker-mongo-1', 27017)
cCryptoPanic = KafkaConsumer('CryptoPanic', bootstrap_servers=['kafka:9093'], api_version=(2,6,0))
cBinance = KafkaConsumer('Binance', bootstrap_servers=['kafka:9093'], api_version=(2,6,0))

#Création de db
db = client.database

#Création de post 
postCryptoPanic = db.posts
postXRP = db.coursXRP
postBTC = db.coursBTC
postETH = db.coursETH

#Fonction définissant si un post est bon ou mauvais
def isGood(votes):
    good = votes["positive"]+votes["saved"]
    bad = votes["disliked"]+votes["negative"]+votes["toxic"]

    if good>bad:
        return 'good'
    else:
        'bad'


def addDataBaseCrypto(msg):
    #récupération du message
    msg.offset
    post = json.loads(msg.value)

    #insértion dans un dataset
    for i in post["post"]:
        ts = time.mktime(datetime.datetime.strptime(i["published_at"], "%Y-%m-%dT%H:%M:%SZ").timetuple())
        if ts >= ((time.time())-(24*3600)):
            i["votes"] = isGood(i["votes"])
            i["published_at"] = ts
            postCryptoPanic.insert_one(i)

    print(db.list_collection_names())
    for postCrypto in postCryptoPanic.find():
        pprint.pprint(postCrypto)

    
    
def addDataBaseBinance(msg):
    #récupération du message
    msg.offset
    data = json.loads(msg.value)

    print(data)
    #insértion dans un dataset

    for i in data["XRP"]:
        coursXRP = {"Timestamp" : i[0] , "open" : i[1], "High" : i[2], "low" : i[3], "close" : i[4], "volume" : i[5]}
        print(coursXRP)
        postXRP.insert_one(coursXRP)

    for j in data["BTC"]:
        coursBTC = {"Timestamp" : j[0] , "open" : j[1], "High" : j[2], "low" : j[3], "close" : j[4], "volume" : i[5]}
        print(coursBTC)
        postBTC.insert_one(coursBTC)

    for k in data["ETH"]:
        coursETH = {"Timestamp" : k[0] , "open" : k[1], "High" : k[2], "low" : k[3], "close" : k[4], "volume" : k[5]}
        print(coursETH)
        postETH.insert_one(coursETH)

def mainCryptoPanic():
    for msg1 in cCryptoPanic:
        addDataBaseCrypto(msg1)

def mainBinance():
    for msg2 in cBinance:
        addDataBaseBinance(msg2)


print("Répondez par 'oui' ou 'non' - Voulez vous supprimez les tables déjà présente dans la bd mongo - cette action est irréversible :")
rep = input()

if rep=="oui":
    postXRP.drop()
    postBTC.drop()
    postETH.drop()
    postCryptoPanic.drop()

#Execution de deux fonction différente en même temps 
#Afin de pouvoir recevoir deux message en même temps
CryptoPanic_thread = threading.Thread(target=mainCryptoPanic)
Binance_thread = threading.Thread(target=mainBinance)

CryptoPanic_thread.start()
Binance_thread.start()

CryptoPanic_thread.join()
Binance_thread.join()