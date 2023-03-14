#!/usr/bin/env python3.9

"""
    mission.py 
    Used to load and manage configuration for a mission
"""

# auxillary libraries
import yaml 

class Mission():

    def __init__(self, path) -> None:
        # members
        self.isValid = True

        # attempt to load in file
        with open(path, "r") as stream:
            try:
                mission_file = yaml.safe_load(stream)
                self.construct_mission(mission_file)
            except Exception as exc:
                self.isValid = False
                print(exc)

    def construct_mission(self, mission_file) -> None:
        # reading in mission values
        self.name = mission_file["mission"]
        self.start = mission_file["mission_date"] + " at " + str(mission_file["mission_start"])
        self.lat = mission_file["mission_start_lat"]
        self.lon = mission_file["mission_start_long"]
        self.location = str(self.lat) + " " + str(self.lon)
        self.duration = str(mission_file["mission_duration"]) + "mins"
        self.operation = str(mission_file["operational_distance"]) + "km"
        
        # reading in manager preferences
        self.darkmode = mission_file["darkmode"]
        self.preloadMap = mission_file["preload_map"]

        # reading in UAV information
        self.UAV_company = mission_file["UAVs"][0]["company"]
        self.UAVNumber = mission_file["UAVs"][0]["number"]
        self.UAVs = mission_file["UAVs"][0]["uavs"]