import requests


"""
id = 1234
suffix = "/vehicles/" + str(id)
print(response = requests.get(url="http://127.0.0.1:5000" + suffix))
print(response.status_code)
"""

"""
id = 0000
suffix = "/getSecurityStatusService"
parameters = {"id": str(id), "responseType": "JSON"}
headers = {"Content-Type":"application/json"}
response = requests.post(url="http://gmapi.azurewebsites.net" + suffix, json=parameters, headers=headers)
data = response.json()
#print(data['data']['doors']['values'][0])
print(data)
"""

"""
id = 1234
suffix = "/vehicles/" + str(id) + "/doors"
response = requests.get(url="http://127.0.0.1:5000" + suffix)
print(response.json())
"""

"""
id = 1234
suffix = "/vehicles/" + str(id) + "/fuel"
response = requests.get(url="http://127.0.0.1:5000" + suffix)
print(response.json())
"""

"""
id = 1234
suffix = "/vehicles/" + str(id) + "/battery"
response = requests.get(url="http://127.0.0.1:5000" + suffix)
print(response.json())
"""
"""
id = 1234
suffix = "/getEnergyService"
parameters = {"id": str(id), "responseType": "JSON"}
headers = {"Content-Type":"application/json"}
response = requests.post(url="http://gmapi.azurewebsites.net" + suffix, json=parameters, headers=headers)
data = response.json()
print(data)
"""
"""

id = 1235
suffix = "/vehicles/" + str(id) + "/engine"
parameters = {"action": "START"}
headers = {"Content-Type":"application/json"}
response = requests.post(url="http://127.0.0.1:5000" + suffix, json=parameters, headers=headers)
print(response.json())

"""


def getVehicleInfo(id):
	data = reqGMApi(id, "/getVehicleInfoService", False)
	vin = data['data']['vin']['value']
	color = data['data']['color']['value']
	drivetrain = data['data']['color']['value']
	is_four_door = data['data']['fourDoorSedan']['value']
	if is_four_door: doorcount = 4
	else: doorcount = 2 
	# Need to email and check what to do if both False/True
	output = {
		"vin": str(vin),
		"color": str(color),
		"doorCount": doorcount,
		"driveTrain": str(drivetrain)
	}
	return output

def reqGMApi(id, suffix, is_startstop):
	if is_startstop: 
		parameters = {"id": str(id), "command": "START_VEHICLE|STOP_VEHICLE", "responseType": "JSON"}
	else:
		parameters = {"id": str(id), "responseType": "JSON"}

	headers = {"Content-Type":"application/json"}
	response = requests.post(url="http://gmapi.azurewebsites.net" + suffix, json=parameters, headers=headers)
	return response.json()

