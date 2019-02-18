
from utilityFunctions import *


try:
	counter = 1
	fakePerson = fakePerson()
	while True:
		changeTorIP()

		# create fake data

		# sendData(targetURL, {})

		print("#" + str(counter))
		counter += 1
except KeyboardInterrupt:
	print(" Terminating...")
	exit()