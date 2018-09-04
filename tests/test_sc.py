from server import *
from unittest.mock import Mock, patch
import json

# Set const real and non-real IDs to be used later
ID_GOOD = 1234
ID_BAD = 0000


def mocktest_setup(func):
	"""
	Helper function for grabbing the mock and output JSON files and parsing them.
	"""
	# Get JSON filenames
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

def test_with_good_id(client):
	"""
	This was a number of very similar functions on first build. I conglomerated them into one, with a single loop through all tested functions.

	Pytest handles this kind of loop well - and will still show each failure - and this seems relatively cleaner than a separate test function
		for each function being tested. 

	Adding another function would be a matter of putting it in the testing_functions list and saving JSONs for the mock and output.

	Mocking the GM API is a more consistent way of testing than testing on the API itself, given a real API will be dynamic and changing.
	"""

	# Functions from server.py to be tested
	testing_functions = [
		'get_vehicle_info',
		'get_security_info',
		'get_fuel',
		'get_battery',
		'start_stop',
	]

	for func in testing_functions:
		# Get mock and expected outputs
		mock_response, correct_output = mocktest_setup(func)

		# Mock the API request made by the function
		with patch('server.requests.post') as mock_get:
			mock_get.return_value.json.return_value = mock_response
			mock_get.return_value.status_code = 200
			
			if func != 'start_stop':
				response = client.get(url_for('endpoints.' + func, id=ID_GOOD))
			else:	# start_stop is a POST endpoint, so needs extra arguments
				headers = {
					'Content-Type': 'application/json'
				}
				parameters = {
					"action": "START"
				}
				response = client.post(url_for('endpoints.' + func, id=ID_GOOD), headers=headers, data=json.dumps(parameters))
		
		# Test output vs. expected output
		assert response.json == correct_output

def test_bad_id_errors():
	return

def test_gmapi_request_response(client):
	"""
	Testing that the GM API is responsive.
	"""
	response = requests.get('http://gmapi.azurewebsites.net')
	assert response.ok == True