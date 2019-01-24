
import random
import string
import json
from datetime import date, datetime

from stem import Signal
from stem.control import Controller
import requests

TorProxyPort = 9050
TorControlPort = 9051
random.seed(datetime.now())


session = requests.session()
session.proxies = {
	'http': "socks5h://localhost:" + str(TorProxyPort),
	'https': "socks5h://localhost:" + str(TorProxyPort)
}

def newSession():
	global session
	session = requests.session()
	session.proxies = {
		'http': "socks5h://localhost:" + str(TorProxyPort),
		'https': "socks5h://localhost:" + str(TorProxyPort)
	}

lastIP = ""
def changeTorIP(TorPass = None):
	with Controller.from_port(port = TorControlPort) as controller:
		if TorPass:
			controller.authenticate(password = TorPass)
		controller.signal(Signal.NEWNYM)

	while True:
		try:
			r = session.get('http://icanhazip.com')
			break
		except requests.exceptions.ConnectionError:
			print("Connect Error #37")
			newSession()

	global lastIP
	if lastIP != r.text:
		print("Using New IP: %s" % r.text)
		lastIP = r.text

def sendData(payload, targetURL):
	while True:
		try:
			r = session.post(targetURL, data=payload)
			break
		except requests.exceptions.ConnectionError:
			print("Connect Error #64")
			newSession()
	return r

def queryWebpage(url, TOR=False, TorPass=None, v=True):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
		'Accept-Language': 'en-US'
	}

	while True:
			if TOR:
				try:
					r = session.get(url, headers=headers, verify=v)
				except requests.exceptions.ConnectionError:
					print("Connect Error #71")
					newSession()
					changeTorIP(TorPass)
			else:
				try:
					r = requests.get(url, headers=headers, verify=v)
				except requests.exceptions.ConnectionError:
					print("Connect Error #77")

			if r.ok:
				return r.text
			else:
				print("received HTTP response: " + str(r.status_code))

def getWebJsonData(url, TOR=False, TorPass=None, v=True):
	while True:
		data = queryWebpage(url, TOR=TOR, TorPass=TorPass, v=v)
		try:
			return json.loads(data)
		except json.decoder.JSONDecodeError:
			print("JSON Error #324")

def createGenericPassword():
	baseURL = 'https://makemeapassword.ligos.net/api/v1/'
	style = random.choice([
		'passphrase',
		'passphrase',
		'passphrase',
		'pin',
		'alphanumeric'
	])

	params = ''
	if style == 'passphrase':
		wc = random.randint(1, 4)
		sp = random.choice(['y', 'n'])
		params = 'pc=1&wc=' + str(wc) + '&sp=' + sp + '&maxCh=32'
	elif style == 'pin':
		l = random.randint(4, 8)
		params = 'l=' + str(l)
	else:	# alphanumeric
		l = random.randint(5, 15)
		sym = random.choice(['y', 'n'])
		params = 'l=' + str(l) + '&sym=' + sym

	url = baseURL + style + '/json?' + params
	while True:
		try:
			r = session.get(url)
			password = json.loads(r.text)["pws"][0]
			if "passphrase could not be found" not in password:
				break
		except json.decoder.JSONDecodeError:
			print("JSON Error #107")
			newSession()
		except requests.exceptions.ConnectionError:
			print("Connect Error #111")
			newSession()

	leet = [
		['i', '1'],
		['l', '1'],
		['e', '3'],
		['a', '4'],
		['s', '5'],
		['t', '7'],
		['o', '0']
	]
	for _ in range(random.randint(0, 7)):
		x = random.choice(leet)
		password = password.replace(x[0], x[1])

	return password

def createMizPawprint(first, last):
	pawprint = first[0] + \
	random.choice(string.ascii_lowercase) + \
	last[0] + \
	random.choice(string.ascii_lowercase + string.digits[1:]) + \
	random.choice(string.ascii_lowercase + string.digits[1:]) + \
	random.choice(string.ascii_lowercase + string.digits[1:])

	return pawprint
	
def createMizEmail(first, last, pawprint):
	if random.randint(0, 100) < 20:
		if random.randint(0, 1):
			user = pawprint[0:1] + last
		else:
			user = first + '.' + last
	else:
		user = pawprint

	if random.randint(0, 100) < 90:
		domain = '@mail.missouri.edu'
	else:
		domain = '@missouri.edu'

	return user + domain

def changeEmailDomain(email):
	domains = [
		"aol.com",
		"att.net",
		"gmail.com",
		"gmx.com",
  		"hotmail.com",
  		"hotmail.co.uk",
  		"icloud.com",
  		"mail.com",
  		"msn.com",
  		"live.com",
  		"yahoo.com",
  		"yahoo.co.uk"
	]

	user = email.split('@')[0]
	return user + '@' + random.choice(domains)

class fakePerson:
	def __init__(self, option = 0):
		self.loadNewPerson(option)

	def loadNewPerson(self, option = 0, gender = 'random', nationality = 'US', onlyASCII = True):
		if option == 0:
			data = getWebJsonData('http://randomuser.me/api/')
			fname = data["results"][0]["name"]["first"]
			lname = data["results"][0]["name"]["last"]
			if onlyASCII:
				fullname = fname + lname
				# While name is non ASCII or contains spaces
				while not all(ord(char) < 128 for char in fullname) or ' ' in fullname:
					data = getWebJsonData('http://randomuser.me/api/')
					fname = data["results"][0]["name"]["first"]
					lname = data["results"][0]["name"]["last"]
					fullname = fname + lname

			self.fname = fname
			self.lname = lname
			self.gender = data["results"][0]["gender"]
			self.email = changeEmailDomain(data["results"][0]["email"])
			self.address = {
				'city': data["results"][0]["location"]["city"],
				'state': data["results"][0]["location"]["state"],
				'zipcode': data["results"][0]["location"]["postcode"],
				'street': data["results"][0]["location"]["street"]
			}
			self.coords = {
				'lat': float(data["results"][0]["location"]["coordinates"]["latitude"]),
				'long': float(data["results"][0]["location"]["coordinates"]["longitude"])
			}
			self.username = data["results"][0]["login"]["username"]
			self.password = data["results"][0]["login"]["password"]
			dob = data["results"][0]["dob"]["date"].split('T')[0].split('-')
			self.birthday = {
				'year': int(dob[0]),
				'month': int(dob[1]),
				'day': int(dob[2])
			}
			self.phonenumber = data["results"][0]["phone"]
			self.nationality = data["results"][0]["nat"]
			self.creditCard = None
			self.MAC = None

		elif option == 1:
			nats = {
				'US': "english-united-states",
				'UK': "english-united-kingdom",
				'DE': "german_germany",
				'ES': "spanish-spain"
			}
			url = 'https://api.namefake.com/' + nats[nationality] + '/' + gender
			data = getWebJsonData(url, v=False)
			while len(data["name"].split(' ')) > 2:
				data = getWebJsonData(url, v=False)
			name = data["name"].split(' ')
			self.fname = name[0]
			self.lname = name[1]
			self.gender = data["url"].split('/')[4]
			self.email = data["email_u"] + '@' + data["email_d"]
			addr = data["address"].split('\n')
			cityState = addr[1].split(',')
			stateZip = cityState[1].split(' ')
			self.address = {
				'city': cityState[0],
				'state': stateZip[1],
				'zipcode': stateZip[2].split('-')[0],
				'street': addr[0]
			}
			self.coords = {
				'lat': data["latitude"],
				'long': data["longitude"]
			}
			self.username = data["username"]
			self.password = data["password"]
			dob = data["birth_data"].split('-')
			self.birthday = {
				'year': int(dob[0]),
				'month': int(dob[1]),
				'day': int(dob[2])
			}
			
			self.phonenumber = data["phone_h"].split('x')[0]
			self.nationality = nationality
			expr = data["cardexpir"].split('/')
			self.creditCard = {
				'number': data["plasticcard"],
				'expr_mo': expr[0],
				'expr_yr': expr[1],
				'ccv': random.randint(100, 999)
			}
			self.MAC = data["macaddress"]

	def getAllData(self):
		return {
			'fname': self.fname,
			'lname': self.lname,
			'email': self.email,
			'address': self.address,
			'coords': self.coords,
			'username': self.username,
			'password': self.password,
			'birthday': self.birthday,
			'phonenumber': self.phonenumber,
			'nationality': self.nationality,
			'creditCard': self.creditCard,
			'MAC': self.MAC
		}

	def getFirstName(self):
		return self.fname

	def getLastName(self):
		return self.lname

	def getEmail(self):
		return self.email

	def getAddress(self):
		return self.address

	def getGeoLocation(self):
		return self.coords

	def getUsername(self):
		return self.username

	def getPassword(self):
		return self.password

	def getBirthday(self):
		return self.birthday

	def getAge(self):
		today = date.today()
		return today.year - self.birthday["year"] - ((today.month, today.day) < (self.birthday["month"], self.birthday["day"]))

	def getPhoneNumber(self):
		return self.phonenumber

	def getNationality(self):
		return self.nationality

	def getCreditCard(self):
		return self.creditCard

	def getMacAddress():
		return self.MAC

