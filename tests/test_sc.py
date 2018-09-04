from server import *
from unittest.mock import Mock, patch
import json

# Set const real and non-real IDs to be used later
ID_GOOD = 1234
ID_BAD = 0000
ID_NOTINT = 'abc'

def test_gmapi_request_response(client):
	"""
	Testing that the GM API is responsive.
	"""
	response = requests.get('http://gmapi.azurewebsites.net')
	assert response.ok == True

def test_bad_url(client):
	"""
	Make sure the app 404's properly
	"""
	response = client.get('/adsflasdf')
	assert response.status_code == 404


"""
The following are each very similar functions to test each endpoint in server.py. The reason for many different functions and not one
	iterative is that this allows more precise identification in pytest. This could still probably be cleaned up and simplified, but
	not a pressing issue.
"""

def test_get_vehicle_info(client):
	mocktest_run(client, 'get_vehicle_info', ID_GOOD)
	mocktest_run(client, 'get_vehicle_info', ID_BAD, 400)
	# Test a non-int id
	mocktest_run(client, 'get_battery', ID_NOTINT, 400)

def test_get_security_info(client):
	mocktest_run(client, 'get_security_info', ID_GOOD)
	mocktest_run(client, 'get_security_info', ID_BAD, 400)

def test_get_fuel(client):
	mocktest_run(client, 'get_fuel', ID_GOOD)
	mocktest_run(client, 'get_fuel', ID_BAD, 400)

def test_get_battery(client):
	mocktest_run(client, 'get_battery', ID_GOOD)
	mocktest_run(client, 'get_battery', ID_BAD, 400)

def test_start_stop(client):
	mocktest_run(client, 'start_stop', ID_GOOD)
	mocktest_run(client, 'start_stop', ID_BAD, 400)


def mocktest_setup(func, id):
	"""
	Helper function for grabbing the mock and output JSON files and parsing them.
	"""

	# Get JSON filenames
	if id == ID_BAD:	# One JSON for all bad id requests as always the same response from GM
		mock_filename = 'mock_bad_id.json'
	else:
		mock_filename = 'mock_' + func + '.json'
	output_filename = 'output_' + func + '.json'

	# Open and parse files
	mock_file = os.path.join(os.path.dirname(__file__), mock_filename)
	output_file = os.path.join(os.path.dirname(__file__), output_filename)
	with open(mock_file, 'r') as f:
		mock_response = json.load(f)
	with open(output_file, 'r') as f:
		correct_output = json.load(f)

	return mock_response, correct_output


def mocktest_run(client, func, id, correct_status=200):
	"""
	Helper function for running mock tests, simulating the GM API

	Mocking the GM API is a more consistent way of testing than testing on the API itself, given a real API will be dynamic and changing.
	"""

	# Prep the mock and output
	mock_response, correct_output = mocktest_setup(func, id)

	# Mock the API request made by the function
	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		mock_get.return_value.status_code = 200
		
		if func != 'start_stop':
			response = client.get(url_for('endpoints.' + func, id=id))
		else:	# start_stop is a POST endpoint, so needs extra arguments
			headers = {
				'Content-Type': 'application/json'
			}
			parameters = {
				"action": "START"
			}
			response = client.post(url_for('endpoints.' + func, id=id), headers=headers, data=json.dumps(parameters))

	# Test output status code vs. expected
	assert response.status_code == correct_status
	
	# Test output vs. expected output if there is output
	if id == ID_GOOD:
		assert response.json == correct_output

