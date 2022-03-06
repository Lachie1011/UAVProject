#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# libraries
import socket
import threading 
import subprocess
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime

from Networking.GCSPublisher import GCSPublisher

# some config 
#Config.set('kivy','window_icon','path/to/icon.ico')

# class - loginApp - initial entry for GCS - checks IP, connects to and launch control functionality
class loginApp(MDApp):

	# title name to ""
	title = ""

	# a function to update the time label
	def time_function(self, dt):

		now = datetime.now()

		current_time = now.strftime("%H:%M:%S")

		self.root.ids.timeLbl.text = current_time

	# function to connect to drone
	def hello_drone(self):

		print("connected to drone!")

	# builds the application
	def build(self):
		
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "BlueGray"

		Clock.schedule_interval(self.time_function, 1)

		return Builder.load_file('login.kv') 

	# ADC threading
	def controlThread(self, name):
		# opening connection to drone
		gcsPublisher = GCSPublisher(self.root.ids.ipAddress.text)

	# on ip text field validation
	def	ip_validate(self, text):

		self.root.ids.spinnerIP.active = True

		validIP = self.checkIP(self.root.ids.ipAddress.text)

		if(not validIP):
			self.root.ids.spinnerIP.active = False
			self.root.ids.ipAddress.text = ""
			return
		#self.root.ids.spinnerIP.active = False

		# Create thread for networking and control 
		try:
   			t1 = threading.Thread(target=self.controlThread, args=("",))
   			t1.start()
		except:
   			print ("Error: unable to start thread")

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

    loginApp().run()


