#!/usr/bin/env python3.9

"""
    UAVApp.py
    Is the main entry point for the UAV Application and sets up the app
"""

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
from kivy.garden.mapview import MapSource, MapMarker

# adding app modules
from mission import Mission

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
		
		# creating mission object
		try:
			self.mission = Mission("missions/" + text + ".yaml")
		except Exception as exc:
			self.root.screens[windows.loginWindow.value].ids.spinner.active = False
			self.root.screens[windows.loginWindow.value].ids.missionTxt.text = ""
			return
		
		# setup manager screen
		if(self.configure_manager()):

			self.root.screens[windows.loginWindow.value].ids.spinner.active = False
			
			# TODO: start manager server/ create manager server

			self.root.current = "Main"
			self.currentFrame = windows.mainWindow.name

	# sets up manager screen
	def configure_manager(self): 

		# update mission values
		self.root.screens[windows.mainWindow.value].ids.missionNameLbl.text += self.mission.name
		self.root.screens[windows.mainWindow.value].ids.missionStart.text += self.mission.start
		self.root.screens[windows.mainWindow.value].ids.missionLocation.text += self.mission.location 
		self.root.screens[windows.mainWindow.value].ids.missionDuration.text += self.mission.duration
		self.root.screens[windows.mainWindow.value].ids.missionOperation.text += self.mission.operation

		# darkmode configuration
		if self.mission.darkmode:
			source = MapSource(url="http://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
					cache_key="darkmap", tile_size=512,
					image_ext="png", attribution="Darkmap")
			self.root.screens[windows.mainWindow.value].ids.map.map_source = source

			# recentering map - when the source changes it loses its initial lat and long 
			self.root.screens[windows.mainWindow.value].ids.map.center_on(self.mission.lat, self.mission.lon)

			# TODO: update this to take in all different maps offered by mapview
			# TODO: if not darkmode should update text label text colour

		# preloading maps
		if self.mission.preloadMap:
			# TODO: figure out how to make api calls around the area and for all zooms? 
			pass

		# load UAVs
		for uav in range(self.mission.UAVNumber):
			# place UAV onto map
			if self.mission.darkmode:
				marker = MapMarker(lat = self.mission.lat, lon = self.mission.lon, source = "images/uav_dark.png")
			else:
				marker = MapMarker(lat = self.mission.lat, lon = self.mission.lon, source = "images/uav_light.png")
			self.root.screens[windows.mainWindow.value].ids.map.add_marker(marker)

			# load callsign information onto screen

		return True


# entry point 
if __name__ == '__main__':

    UAVApp().run()


