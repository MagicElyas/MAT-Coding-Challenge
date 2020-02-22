import paho.mqtt.client as mqtt  #import the client1
import time

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
        client.subscribe(topic = 'carCoordinates')
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
  print('-----------------')
  print('topic: '+ str(message.topic) )
  print('payload: '+ str(message.payload) )
  print('qos: '+ str(message.qos) )

def connect_to_broker(broker):
  mqtt.Client.connected_flag=False
  client = mqtt.Client("mat_app") 
  client.on_connect=on_connect
  client.on_message=on_message
  client.connect(broker)      
  client.loop_forever()

connect_to_broker('127.0.0.1')