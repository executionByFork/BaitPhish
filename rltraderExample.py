
from utilityFunctions import *
from bs4 import BeautifulSoup


def checkSuccess(data):
	try:
		j = json.loads(data)
	except json.decoder.JSONDecodeError:
		return "HTML recieved"

	return j["status"]


targetURL = "https://rltrader-lounge.com/openid"
counter = 0
person = fakePerson()

while True:
	try:
		counter += 1
		changeTorIP()

		html = queryWebpage(targetURL, TOR=True)
		soup = BeautifulSoup(html, 'html.parser')
		tag = soup.find(attrs={"name": "_token"})
		token = str(tag).split('"')[5]
		person.loadNewPerson()

		headers = {
			'User-Agent': createUserAgent(),
			'Accept-Language': "en-US",
			'Referer': targetURL
		}
		guardCode = genAlphanumeric(5)

		print("#" + str(counter))
		print("token: " + token)
		print("user: " + person.getUsername())
		print("pass: " + person.getPassword())
		print("guardCode: " + guardCode)

		r = sendData(
			targetURL + "/check",
			{
				'_token': token,
				'username': person.getUsername(),
				'password': person.getPassword()
			},
			headers = headers)

		print("POST check: " + checkSuccess(r.text))

		r = sendData(
			targetURL + "/login",
			{
				'_token': token,
				'username': person.getUsername(),
				'password': person.getPassword(),
				'guard': guardCode,
				'ref': ""
			},
			headers = headers)
		print("POST submit: " + checkSuccess(r.text) + '\n')

	except KeyboardInterrupt:
		print(" Terminating...")
		exit()
