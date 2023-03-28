"""
    mission.py 
    Used to load and manage configuration for a mission
"""

import yaml 

class Mission():
    """
        creates and holds information relevant to the mission
    """
    def __init__(self, path) -> None:
        # valid mission flag
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
        """ constructs the mission from yaml file"""
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
    
    def update_location(self, callsign, lat, long) -> bool:
        """ updates the current location for a UAV """
        if not (lat.isnumeric() and long.isnumeric()):
            return False
        
        for i in range(len(self.UAVs)):
            if self.UAVs[i]["callsign"] == callsign:
                self.UAVs[i]["location"] = [float(lat), float(long)]
                return True        
        
        return False