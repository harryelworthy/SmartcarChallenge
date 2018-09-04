"""
Tests as were previously formatted. Leaving here in case I want to revert to more disparate testing.
"""


def test_vehicle_info(client):
	mock_file = 'mock_vehicleinfo.json'
	output_file = 'output_vehicleinfo.json'
	mock_response, correct_output = mocktest_setup(mock_file, output_file)

	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		response = client.get(url_for('endpoints.get_vehicle_info', id=ID_GOOD))
	
	assert response.json == correct_output

def test_security_info(client):
	mock_file = 'mock_securityinfo.json'
	output_file = 'output_securityinfo.json'
	mock_response, correct_output = mocktest_setup(mock_file, output_file)

	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		response = response = client.get('/vehicles/' + str(ID_GOOD) + '/doors')
	
	assert response.json == correct_output

def test_fuel(client):
	mock_file = 'mock_fuelbattery.json'
	output_file = 'output_fuel.json'
	mock_response, correct_output = mocktest_setup(mock_file, output_file)

	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		response = client.get('/vehicles/' + str(ID_GOOD) + '/fuel')
	
	assert response.json == correct_output

def test_battery(client):
	mock_file = 'mock_fuelbattery.json'
	output_file = 'output_battery.json'
	mock_response, correct_output = mocktest_setup(mock_file, output_file)

	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		response = client.get('/vehicles/' + str(ID_GOOD) + '/battery', )

	assert response.json == correct_output

def test_start_stop(client):
	mock_file = 'mock_engine.json'
	output_file = 'output_engine.json'
	mock_response, correct_output = mocktest_setup(mock_file, output_file)

	headers = {
		'Content-Type': 'application/json'
	}

	parameters = {
		"action": "START"
	}

	with patch('server.requests.post') as mock_get:
		mock_get.return_value.json.return_value = mock_response
		response = client.post('/vehicles/' + str(ID_GOOD) + '/engine', headers=headers, data=json.dumps(parameters))

	assert response.json == correct_output