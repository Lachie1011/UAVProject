#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# importing some libraries
import time
import numpy as np
import paho.mqtt.client as paho

def on_message(mosq, obj, msg):

    print(str(msg.payload))

def on_publish(mosq, obj, mid):
    pass

if __name__ == '__main__':

    client = paho.Client()
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect("127.0.0.1", 1883, 60)

    client.subscribe("~/control/thrust", 0)
    client.subscribe("~/control/button", 0)
    client.subscribe("~/control/pitch", 0)
    client.subscribe("~/control/roll", 0)
    client.subscribe("~/control/yaw", 0)

    while client.loop() == 0:
        pass
