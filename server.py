import os
import requests
from flask import Flask, render_template, jsonify, abort, url_for, Blueprint
from flask import request as flaskreq

BASE_URL = 'http://gmapi.azurewebsites.net' 

bp = Blueprint('endpoints', __name__)	# How flask handles URL routing. Using a blueprint allows URLs to carry through even in testing.


def request_GM_api(id, suffix, add_params={}):
	'''
	General use function for requests to the GM api to minimize code reuse. This is used at the start of each endpoint function.
	suffix is the URL suffix needed for each request
	add_params are any additional parameters needed to pass to GM, in this case this is used by the Start/Stop function to pass the action required
	'''

	# Prep request
	headers = {'Content-Type':'application/json'}
	parameters = {'id': str(id), 'responseType': 'JSON'}
	parameters.update(add_params)

	# Make request
	response = requests.post(url=BASE_URL + suffix, json=parameters, headers=headers)

	# Check that GM provided a good response
	if response.status_code != 200:
		abort(500, 'GM server gave error code ' + response.status_code)

	return response.json()


@bp.route('/vehicles/<id>', methods=['GET'])
def get_vehicle_info(id):
	'''
	Vehicle Info endpoint. GET request that sits at /vehicles/:id.
	
	Request:
	GET /vehicles/:id

	Response:
	{
	  "vin": "1213231",
	  "color": "Metallic Silver",
	  "doorCount": 4,
	  "driveTrain": "v8"
	}
	'''
	check_id(id)
	data = request_GM_api(id, '/getVehicleInfoService')

	# Get data from dict pulled from JSON
	vin = data['data']['vin']['value']
	color = data['data']['color']['value']
	drivetrain = data['data']['driveTrain']['value']
	is_four_door = data['data']['fourDoorSedan']['value']
	# Establish number of doors
	if is_four_door: doorcount = 4
	else: doorcount = 2 
	# TODO Need to email and check what to do if both False/True
	
	# Put response into output format
	response = {
		'vin': str(vin),
		'color': str(color),
		'doorCount': doorcount,
		'driveTrain': str(drivetrain)
	}

	return jsonify(response)

@bp.route('/vehicles/<id>/doors', methods=['GET'])
def get_security_info(id):
	"""
	Vehicle Security endpoint. GET request that sits at /vehicles/:id.
	
	Request:
	GET /vehicles/:id/doors

	Response:
	[
	  {
	    "location": "frontLeft",
	    "locked": true
	  },
	  {
	    "location": "frontRight",
	    "locked": true
	  }
	]
	"""
	check_id(id)
	data = request_GM_api(id, '/getSecurityStatusService')

	# Set both outputs to None, to be output in case of inadequate info from GM
	# TODO check this
	left_locked = None
	right_locked = None

	# Iterate through doors, getting lock values for front left and right
	door_list = data['data']['doors']['values']
	for door in door_list:
		if door['location']['value'] == 'frontLeft':
			left_locked = door['locked']['value'] == 'True'
		elif door['location']['value'] == 'frontRight':
			right_locked = door['locked']['value'] == 'True'
	# WHAT TO DO IF EITHER IS NONE?
	# TODO Need to lowercase output

	# Put response into output format
	response = [
	{
		'location': 'frontLeft',
		'locked': left_locked
	},
	{
		'location': 'frontRight',
		'locked': right_locked
	}]

	return jsonify(response)

@bp.route('/vehicles/<id>/fuel', methods=['GET'])
def get_fuel(id):
	"""
	Vehicle Fuel endpoint. GET request that sits at /vehicles/:id/fuel. 
	
	Request:
	GET /vehicles/:id/fuel

	Response:
	{
	  "percent": 30
	}
	"""
	check_id(id)
	data = request_GM_api(id, '/getEnergyService')

	# Get fuel data, format, send response
	fuel = int(data['data']['tankLevel']['value'])
	response = {
		'percent': fuel,
	}
	return jsonify(response)

@bp.route('/vehicles/<id>/battery', methods=['GET'])
def get_battery(id):
	"""
	Vehicle Battery endpoint. GET request that sits at /vehicles/:id/battery.
	
	Request:
	GET /vehicles/:id/battery

	Response:
	{
	  "percent": 50
	}
	"""
	check_id(id)
	data = request_GM_api(id, '/getEnergyService')

	# Get battery data, format, send response
	battery = int(data['data']['batteryLevel']['value'])
	response = {
		'percent': battery,
	}
	return jsonify(response)

@bp.route('/vehicles/<id>/engine', methods=['POST'])
def start_stop(id):
	"""
	Vehicle Start/Stop endpoint. POST request that sits at /vehicles/:id/engine, takes an action and provides the outcome. 
	
	Request:
	POST /vehicles/:id/engine
	Content-Type: application/json

	{
	  "action": "START|STOP"
	}

	Response:
	{
	  "status": "success|error"
	}
	"""
	check_id(id)

	# Check that POST request is reasonable
	if not flaskreq.json:
		abort(400, 'Non-JSON POST request')

	# Check if starting or stopping engine, send to relevant function
	command = ''
	if flaskreq.json['action'] == 'START':
		command = 'START_VEHICLE'
	elif flaskreq.json['action'] == 'STOP':
		command = 'STOP_VEHICLE'
	else:
		abort(400, 'Command not recognized. Accepts START|STOP')

    # Attempt Start/Stop
	data = request_GM_api(id, '/actionEngineService', {'command': command})

	# Receive, process and send response
	if data['actionResult']['status'] == 'EXECUTED':
		status = 'success'
	elif data['actionResult']['status'] == 'FAILED':
		status = 'error'
	else:
		abort(500, 'Error with GM response')

	response = {
		'status': status,
	}

	return jsonify(response)


def create_app():
	"""
	Needed for pytest to work. Creates flask app.
	"""
	app = Flask(__name__)
	app.register_blueprint(bp)	# Allows URLs to carry through in testing
	return app

def check_id(id):
	if !isinstance(id, int): 
		abort(400, 'Non-int ID')


if __name__ == '__main__':
	app = create_app()
	app.run(port=os.getenv('PORT', 5000))