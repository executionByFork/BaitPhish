
from utilityFunctions import *
import os

TorPass = os.environ['TORPASS']

try:
	counter = 1
	fakePerson = fakePerson()
	while True:
		changeTorIP(TorPass)

		# create fake data

		# sendData({}, targetURL)

		print("#" + str(counter))
		counter += 1
except KeyboardInterrupt:
	print(" Terminating...")
	exit()