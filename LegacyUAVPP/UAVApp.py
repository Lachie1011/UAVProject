#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# auxillary libraries
import cv2
import socket
import threading 
import subprocess
import numpy as np 
from enum import Enum
from datetime import datetime

# kivy libraries
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen 

# module libraries 
from Networking.GCSPublisher import GCSPublisher
from Networking.GCSImageGenerator import GCSImageGenerator

# window Enum class
class windows(Enum):
	loginWindow = 0
	mainWindow = 1

# login window class
class LoginWindow(Screen):
	pass

# main window class
class MainWindow(Screen):
	pass

# window manager
class WindowManager(ScreenManager): 
	pass

# class - UAVApp
class UAVApp(MDApp):

	# current frame
	currentFrame = windows.loginWindow.name

	# window configuration 
	Window.maximize()

	# builds the application
	def build(self):
		
		# layout options
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"

		# creating capture for imagery
		self.capture = cv2.VideoCapture(0)

		# scheduling camera capture
		Clock.schedule_interval(self.frameCapture, 1/60)

		# scheduling indicator updates
		Clock.schedule_interval(self.indicatorUpdate, 1/60)

		# scheduling time clock
		Clock.schedule_interval(self.timeFunction, 1)	

		return Builder.load_file('UAVApp.kv') 

	# a function to capture frames from the receiver
	def frameCapture(self, dt):
		
		if(self.currentFrame == windows.mainWindow.name):

			# get frame
			ret, self.frame = self.capture.read()

			if(ret):
				self.root.screens[windows.mainWindow.value].ids['imageFrame'].texture = self.getTextureFromFrame(self.frame, 0) # update texture

	# a function to capture frames from the receiver
	def indicatorUpdate(self, dt):
		
		if(self.currentFrame == windows.mainWindow.name):

			# reading in indicator images  
			throttle = cv2.imread("generatedImages/throttle.png")
			#joystick = cv2.imread("generatedImages/joystick.png")

			# updating onscreen images 
			retThrottle = self.getTextureFromFrame(throttle, 0) 

			if(retThrottle != -1):
				self.root.screens[windows.mainWindow.value].ids['imageThrottle'].texture = retThrottle
			
			#self.root.screens[windows.mainWindow.value].ids['imageJoystick'].texture = self.getTextureFromFrame(joystick, 0) 

	# this function get the texture for the image
	def getTextureFromFrame(self, frame, flipped):

		bufferFrame = cv2.flip(frame, flipped)

		if(bufferFrame is None):
			return -1 

		bufferFrameStr = bufferFrame.tostring()
		
		imageTexture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
		imageTexture.blit_buffer(bufferFrameStr, colorfmt='bgr', bufferfmt='ubyte')
		
		return imageTexture

	# a function to update the time label
	def timeFunction(self, dt):

		if(self.currentFrame == windows.loginWindow.name):
			now = datetime.now()

			current_time = now.strftime("%H:%M:%S")

			#self.root.ids.timeLbl.text = current_time
			self.root.screens[windows.loginWindow.value].ids.timeLbl.text = current_time # todo: make this an enum 

		if(self.currentFrame == windows.mainWindow.name):
			now = datetime.now()

			current_time = now.strftime("%H:%M:%S")

			#self.root.ids.timeLbl.text = current_time
			self.root.screens[windows.mainWindow.value].ids.timeLbl.text = current_time # todo: make this an enum 

	# ADC threading
	def controlThread(self, name):
		# opening connection to drone
		gcsPublisher = GCSPublisher(self.root.screens[windows.loginWindow.value].ids.ipAddress.text)

	# image generator threading
	def imageGenThread(self, name):
		# opening connection to drone
		indicatorUpdator = GCSImageGenerator("127.0.0.1")
		indicatorUpdator.start()

	# on ip text field validation
	def	ip_validate(self, text):

		self.root.screens[windows.loginWindow.value].ids.spinnerIP.active = True

		validIP = self.checkIP(self.root.screens[windows.loginWindow.value].ids.ipAddress.text)

		if(not validIP):
			self.root.screens[windows.loginWindow.value].ids.spinnerIP.active = False
			self.root.screens[windows.loginWindow.value].ids.ipAddress.text = ""
			return
		
		self.root.screens[windows.loginWindow.value].ids.spinnerIP.active = False
		
		# Create thread for networking and control 
		try:
			indicatorThread = threading.Thread(target=self.imageGenThread, args=("",))
			indicatorThread.start()

			controlThread = threading.Thread(target=self.controlThread, args=("",))
			controlThread.start()
		except:
			print ("Error: unable to start thread")

		self.root.current = "Main"
		self.currentFrame = windows.mainWindow.name

	# checking the ip address
	def checkIP(self, text):

		st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		try:
			st.connect((text, 1))
			IP = st.getsockname()[0]
			return True
		
		except:
			return False

# entry point 
if __name__ == '__main__':

    UAVApp().run()


