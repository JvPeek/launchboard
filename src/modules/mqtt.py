import configtester as config
import random
import paho.mqtt.client as mqtt

configData = config.getMqttCredentials()
clientConnected = 0

def on_connect(client, userdata, flags, rc):
    global clientConnected
    if rc == 0:
        print("Connected to MQTT Broker!")
        clientConnected = 1
    else:
        print("Failed to connect, return code %d\n", rc)
        clientConnected = 0
   

def on_disconnect(client, userdata, rc):
   global clientConnected
   clientConnected = 0
   print ("Lost connection, return code &d\n", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
def connect():
    global client
    try:
        client.connect(configData["broker"],configData["port"])
    except:
        print ("connection failed")

def sendMessage(messageData):
    global client
    client.publish(messageData[0], messageData[1])
def thread(mqttQueue):

    while True:
        if (not clientConnected):
            connect()

        client.loop()
        messageToSend = mqttQueue.get()
        if (messageToSend):
            sendMessage(messageToSend)




