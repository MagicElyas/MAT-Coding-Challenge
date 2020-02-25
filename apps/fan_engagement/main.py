import time
import json
import paho.mqtt.client as mqtt  #import the client1
from models.race import Race


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
        client.subscribe(topic = 'carCoordinates')
    else:
        print("Bad connection Returned code=",rc)


def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    userdata.update_car_info(payload)


def connect_to_broker(broker, broker_port):
    mqtt.Client.connected_flag=False
    client = mqtt.Client("mat_app")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port = broker_port)
    race = Race(client,'carStatus', 'events')
    print(type(client))
    client.user_data_set(race)
    client.loop_forever()


connect_to_broker('127.0.0.1', 1883)