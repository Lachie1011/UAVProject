#!/usr/bin/env python3.9

# adding sub-modules
import sys
sys.path.append('../')

# auxillary libraries
import yaml
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
from kivy.garden.mapview import MapSource

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

		# scheduling time clock
		Clock.schedule_interval(self.timeFunction, 1)	

		return Builder.load_file('UAVApp.kv') 

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

	# validates the mission file 
	def	mission_validate(self, text):
		self.root.screens[windows.loginWindow.value].ids.spinner.active = True

		validMission = self.setup_mission("missions/" + text + ".yaml")
		if(not validMission):
			self.root.screens[windows.loginWindow.value].ids.spinner.active = False
			self.root.screens[windows.loginWindow.value].ids.missionTxt.text = ""
			return
		
		self.root.screens[windows.loginWindow.value].ids.spinner.active = False
		
		# TODO: start manager server/ create manager server

		self.root.current = "Main"
		self.currentFrame = windows.mainWindow.name

	# gets mission and sets up mission screen
	def setup_mission(self, missionPath): 
		# mission file
		with open(missionPath, "r") as stream:
			try:
				self.mission = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				print(exc)
				return False
			
		# update mission values
		self.root.screens[windows.mainWindow.value].ids.missionNameLbl.text += self.mission["mission"]
		self.root.screens[windows.mainWindow.value].ids.missionStart.text += self.mission["mission_date"] + " at " + str(self.mission["mission_start"])
		self.root.screens[windows.mainWindow.value].ids.missionLocation.text += str(self.mission["mission_start_location"])
		self.root.screens[windows.mainWindow.value].ids.missionDuration.text += str(self.mission["mission_duration"]) + "mins"
		self.root.screens[windows.mainWindow.value].ids.missionOperation.text += str(self.mission["operational_distance"]) + "km"

		# updating map to darkmode
		source = MapSource(url="http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
                   cache_key="darkmap", tile_size=512,
                   image_ext="png", attribution="Darkmap")
		
		self.root.screens[windows.mainWindow.value].ids.map.map_source = source

		return True


# entry point 
if __name__ == '__main__':

    UAVApp().run()


