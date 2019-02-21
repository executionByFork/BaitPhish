
from utilityFunctions import *

targetURL = 'https://antiphish.herokuapp.com/auth.php'

try:
	counter = 1
	fakePerson = fakePerson()
	while True:

		r = sendData(targetURL, {
			'username': fakePerson.getUsername(),
			'password': fakePerson.getPassword(),
			'token': '9fdW9Kqo35l1hsocDx21'
		}, TOR=False)

		print("#" + str(counter))
		print(r.text)

		counter += 1
		fakePerson.loadNewPerson()
except KeyboardInterrupt:
	print(" Terminating...")
	exit()