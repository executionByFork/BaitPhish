
from utilityFunctions import *

targetURL = 'https://owa-storage-accessss3.webnode.com'

try:
	counter = 1
	fakePerson = fakePerson()
	while True:
		changeTorIP()
		password = createGenericPassword()
		fakePerson.loadNewPerson()
		first = fakePerson.getFirstName()
		last = fakePerson.getLastName()
		pawprint = createMizPawprint(first, last)
		email = createMizEmail(first, last, pawprint)

		# sendData({
		# 	'wnd_ShortTextField_353664': pawprint,
		# 	'wnd_ShortTextField_814166': password,
		# 	'wnd_ShortTextField_12047': email,
		# 	'send': 'wnd_FormBlock_207467',
		# }, targetURL)

		print("#" + str(counter))
		print("User: " + pawprint)
		print("Email: " + email)
		print("Pass: " + password + "\n")
		counter += 1
except KeyboardInterrupt:
	print(" Terminating...")
	exit()