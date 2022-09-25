#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# importing some libraries
import cv2
import time
import numpy as np
import paho.mqtt.subscribe as paho

# subscriber class that generates images to be used for control indication 
class GCSImageGenerator: 

    # inital function
    def __init__(self, ip):

        self.host = ip 
        self.prevState = [0,0,0,0,0]
    
    # function to run the generation
    def start(self):
        
        while(True):

            # get current data 
            state = self.getData()

            # only generate new images if new data
            if(state != self.prevState):

                # only need the first value for the throttle
                self.updateThrottle(state[0])

                # update the joystick with the rest 
                self.updateJoystick(state)

                # update preevious state
                self.prevState = state

    # function that gets data
    def getData(self):

        # simple subscriptions to just get data once 
        self.thrust = paho.simple("~/control/thrust", hostname = self.host)
        self.button = paho.simple("~/control/button", hostname = self.host)
        self.pitch = paho.simple("~/control/pitch", hostname = self.host)
        self.roll = paho.simple("~/control/roll", hostname = self.host)
        self.yaw = paho.simple("~/control/yaw", hostname = self.host)

        return [self.thrust.payload, self.button.payload, self.pitch.payload, self.roll.payload, self.yaw.payload]

    # function to update throttle 
    def updateThrottle(self, level):

        # getting base image
        baseImage = cv2.imread("../UAVAPP/generatedImages/baseThrottle.png")

        # calculating level in image 
        starty = round((1 - int(level.decode("utf-8")) / 100) * 281)

        # fill colour 
        colour = (68, 185, 223)

        # rectangle points
        startPoint = (4,starty)
        endPoint = (139, 281)

        # drawing throttle level 
        throttleImage = cv2.rectangle(baseImage, startPoint, endPoint, colour, -1) 

        # updating joysick image 
        cv2.imwrite("../UAVAPP/generatedImages/throttle.png", throttleImage)
    
    # function to update joystick
    def updateJoystick(self, state):
        pass
    
    # function to print the state of the data
    def printState(self):

        print(self.thrust.payload)
        print(self.button.payload)
        print(self.pitch.payload)
        print(self.roll.payload)
        print(self.yaw.payload)

# main entry point
def main():
    imageGen = GCSImageGenerator("127.0.0.1") 
    imageGen.start()

if __name__ == "__main__":
    main()