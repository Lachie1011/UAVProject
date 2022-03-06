#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

####### API #######

# Channel 0: throttle 	-> motor speed 
# Channel 1: joystick Y -> pitch
# Channel 2: joystick X -> roll
# Channel 3: joystick Z -> yaw
# Channel 4: Button 	-> button 

####### END #######

# Libraries
import time
import busio
import digitalio
import board
import numpy as np
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# ADC class
class ADC:

	# initial function
	def __init__(self):

		# create the spi bus)
		spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

		# create the cs (chip select)
		cs = digitalio.DigitalInOut(board.CE0)

		# create the mcp object
		mcp = MCP.MCP3008(spi, cs)

		# creating analog input channels
		self.chan0 = AnalogIn(mcp, MCP.P0)
		self.chan1 = AnalogIn(mcp, MCP.P1)
		self.chan2 = AnalogIn(mcp, MCP.P2)
		self.chan3 = AnalogIn(mcp, MCP.P3)
		self.chan4 = AnalogIn(mcp, MCP.P4)

		self.state = np.array([0,0,0,0,0])		

	# a function to normalise a value between 0 -> 100
	def normalise(self, value):

		max = 65000

		normalised = (value/max) * 100

		# accounting for drift
		if normalised > 48 and normalised < 53:
			normalised = 50

		return int(normalised)	

	# getting state of controls
	def GetState(self):

		self.state = np.array([
			self.normalise(self.chan0.value), 
			self.normalise(self.chan1.value), 
			self.normalise(self.chan2.value), 
			self.normalise(self.chan3.value), 
			self.normalise(self.chan4.value)])

		return self.state
# Main
def Main():
	
	print("[INFO] This is to be used as a library not a .exe")

if __name__ == "__main__":
	Main()