#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# importing some libraries
import time
import numpy as np
import paho.mqtt.publish as publish

# importing ADC functionality 
from GCSControl.ADC import ADC

# GCSPublisher class
class GCSPublisher:

    # host ip address
    host = "localhost"

    #initial function
    def __init__(self, ip):

        self.host = ip

        self.adc = ADC()
        self.state = np.array([0,0,0,0,0])      

        self.publishControls()

    # publishing function 
    def publishControls(self):

        while(True):
            
            # getting state of controls
            self.state = self.adc.GetState()

            controlMsgs = [{'topic': "~/heartbeat", 'payload': '0'},
                {'topic': "~/control/thrust", 'payload': str(self.state[0])},
                {'topic': "~/control/pitch", 'payload': str(self.state[1])},
                {'topic': "~/control/roll", 'payload': str(self.state[2])},
                {'topic': "~/control/yaw", 'payload': str(self.state[3])}, 
                {'topic': "~/control/button", 'payload': str(self.state[4])}]

            # publish ADC data
            publish.multiple(controlMsgs, hostname = self.host)            

# Main 
def Main():
    gcsPublisher = GCSPublisher()

if __name__ == '__main__':
    Main()

