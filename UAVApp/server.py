"""
    server.py
    Runs the flask server for the application and outlines the routes
"""

from flask import Flask, Response, jsonify
 
# flask app
app = Flask(__name__)

# mission in use
mission = None

class Server:
    """
        creates a flask server and manages routing
    """
    def __init__(self, _mission) -> None:
        global mission  # global mission 
        mission = _mission
        self.__port = 8500  # TODO: port should be read from mission file and passed into this server

    @app.route('/', methods=['GET'])
    def index() -> Response:
        """ index endpoint """
        data = {'data': ''}
        return jsonify(data), 200

    @app.route('/update/location/', methods=['POST'])  # <callsign>@<lat><long>
    def update_location() -> Response: 
        """ endpoint to update the location of a UAV """
        data = {'data': ''}
        
        if mission.update_location():
            data = {'data': 'updated successfully'}
            return jsonify(data), 200
        return jsonify(data), 400


    @app.route('/update/fuel/', methods=['POST'])  # <callsign>@<fuel>
    def update_fuel() -> Response: 
        """ endpoint to update the fuel of a UAV """
        pass

    def run(self):
        app.run(port=self.__port)
