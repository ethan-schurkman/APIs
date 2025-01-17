from urllib.parse import urlencode
from httplib2 import Http
import json
import sys
import base64


print("Running Endpoint Tester....\n")
address = input("Please enter the address of the server you want to access, \n If left blank the connection will be set to 'http://localhost:5000':   ")
if address == '':
	address = 'http://localhost:5000'

#TEST 1: TRY TO REGISTER A NEW USER 
try:
	h = Http()
	url = address + '/users'
	data = dict(username="Peter", password="Pan")
	data = json.dumps(data)
	resp, content = h.request(url,'POST', body = data, headers = {"Content-Type": "application/json"})
	if resp['status'] != '201' and resp['status'] != '200':
 		raise Exception('Received an unsuccessful status code of %s' % resp['status'])

except Exception as err:
	print("Test 1 FAILED: Could not make a new user")
	print(err.args)
	sys.exit()
else:
	print("Test 1 PASS: Succesfully made a new user")

#TEST 2: OBTAIN A TOKEN
try:
	h = Http() 
	h.add_credentials('Peter','Pan')
	url = address + '/token'
	resp, content = h.request(url,'GET' , headers = {"Content-Type" : "application/json"})
	if resp['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % resp['status'])
	new_content = json.loads(content)
	if not new_content['token']:
		raise Exception('No Token Received!')
	token = new_content['token']
	print("received token: %s" % token)
except Exception as err:
	print("Test 2 FAILED: Could not exchange user credentials for a token")
	print(err.args)
	sys.exit()
else:
	print("Test 2 PASS: Succesfully obtained token! ")

#TEST 3: TRY TO ADD PRODUCS TO DATABASE

try:
	h = Http()
	h.add_credentials(token,'blank')
	url = address + '/products'
	data = dict(name = "apple", category = "fruit", price= "$.99")
	resp, content = h.request(url,'POST', body = json.dumps(data), headers = {"Content-Type" : "application/json"})
	if resp['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
	print("Test 3 FAILED: Could not add new products")
	print(err.args)
	sys.exit()
else:
	print("Test 3 PASS: Succesfully added new products")


#TEST 4: TRY ACCESSING ENDPOINT WITH AN INVALID TOKEN
try:
	h = Http()
	tmp = token
	token = 'do-not-pass'
	h.add_credentials(token,'blank')
	url = address + '/products'
	resp, content = h.request(url,'GET', headers={"Content-Type" : "application/json"})
	if resp['status'] == '200':
		raise Exception('Received successful 200 code')
	token = tmp
except Exception as err:
	print("TEST 4 Failed. Able to access endpoint with invalid token")
	print(err.args)
	sys.exit()
else:
	print("Test 4 Pass: Successfully verified we cannot access products with an invalid token.")

#TEST 5: TRY TO VIEW ALL PRODUCTS IN DATABASE
try:
	h = Http()
	h.add_credentials(token,'blank')
	url = address + '/products'
	resp, content = h.request(url,'GET', headers={"Content-Type" : "application/json"})
	if resp['status'] != '200':
		raise Exception("Received unsucessful code not equal to 200")
except Exception as err:
	print("Test 5 Failed. Could not view all products in DB")
	print(err.args)
	sys.exit()
else:
	print("Test 5 Pass: Successfully verified we can access all products with a valid token")

#TEST 6: TRY TO VIEW A SPECIFIC CATEGORY OF PRODUCTS
try:
	h = Http()
	h.add_credentials(token,'blank')
	url = address + '/products/fruit'
	resp, content = h.request(url,'GET', headers={"Content-Type" : "application/json"})
	if resp['status'] != '200':
		raise Exception("Received unsuccessful code of %s" % resp['status'])
except Exception as err:
	print("Test 6 failed. Could not view a product via a category")
	print(err.args)
	sys.exit()
else:
	print("Test 6 PASS: successfully verified we can view products via category")
