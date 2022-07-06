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
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen 

# module libraries 
from Networking.GCSPublisher import GCSPublisher

# Window Enum class
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

	# builds the application
	def build(self):
		
		# layout options
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"

		# creating capture for imagery
		self.capture = cv2.VideoCapture(0)

		# scheduling image clock
		Clock.schedule_interval(self.frame_capture, 1/30.0)

		# scheduling time clock
		Clock.schedule_interval(self.time_function, 1)	

		return Builder.load_file('UAVApp.kv') 


	# a function to capture frames from the receiver
	def frame_capture(self, dt):
		
		if(self.currentFrame == windows.mainWindow.name):

			# get frame
			ret, frame = self.capture.read()

			if(ret):

				bufferFrame = cv2.flip(frame, 0)	
				bufferFrameStr = bufferFrame.tostring()

				imageTexture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt = 'bgr')
				imageTexture.blit_buffer(bufferFrameStr, colorfmt = 'bgr', bufferfmt = 'ubyte')

				self.root.screens[windows.mainWindow.value].ids['imageFrame'].texture = imageTexture # update texture

				print(self.root.screens[windows.mainWindow.value].ids['imageFrame'].texture) # = imageTexture # update texture

	# a function to update the time label
	def time_function(self, dt):

		if(self.currentFrame == windows.loginWindow.name):
			now = datetime.now()

			current_time = now.strftime("%H:%M:%S")

			#self.root.ids.timeLbl.text = current_time
			self.root.screens[windows.loginWindow.value].ids.timeLbl.text = current_time # todo: make this an enum 

	# ADC threading
	def controlThread(self, name):
		# opening connection to drone
		gcsPublisher = GCSPublisher(self.root.screens[windows.loginWindow.value].ids.ipAddress.text)

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
		#try:
   		#	t1 = threading.Thread(target=self.controlThread, args=("",))
   		#	t1.start()
		#except:
   		#	print ("Error: unable to start thread")
		
		self.root.switch_to(self.root.screens[windows.mainWindow.value])
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


