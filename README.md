# BaitPhish
### _Bait (verb): To deliberately annoy or taunt_
#### A way to give back to the Phishers

This project is a scripting library that can be used to quickly generate a bunch of fake but realistic looking data. The purpose of this project is to provide an easy to use tool for fighting back at phishing scams. Using these functions, you can generate and send out loads of fake user data, and flood the logs of the scammers who are trying to steal your information with useless bait.

By successfully using this tool to create a script, not only will you make the bulk data they collect much harder to use or sell, but more importantly you will feel satisfaction from knowing that you have just become an enourmous pain in the phisher's ass.

## Setup Instructions for Linux based operating systems

1) Setup a virtual environment for python3
  - Install [`python3`](https://docs.python-guide.org/starting/install3/linux/), and [`pip`](https://packaging.python.org/guides/installing-using-linux-tools/) if they are not already installed on your system
  - Install [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) for easy management of your python virutal environments
  - Create a new virtual environment with the command `mkvirtualenv <name>` using a name of your choice
2) Install required packages
  - Activate your virutal environment with `workon <name>`
  - Install the following packages with `pip install <package>` at the listed or newer version
```
beautifulsoup4==4.7.1
certifi==2018.10.15
chardet==3.0.4
fake-useragent==0.1.11
idna==2.7
PySocks==1.6.8
requests==2.20.1
soupsieve==1.7.3
stem==1.7.0
urllib3==1.24.1
```
3) You can now begin writing a script using the functions and classes provided in `utilityFunctions.py`. Use the provided `startTemplate.py` script for boilerplate code.

## Setup Instructions for Windows operating systems

1) Good luck

#### Documentation on the available functions, classes, and methods in `utilityFunctions.py` can be found [here](Documentation.md)

Once you have set up the tool, you may test it on a dummy webpage instance [here](https://antiphish.herokuapp.com/). The site simply returns either success or an error, depending on whether you've sent the data in the right format.  
_Think you have the right format and are still getting an error response? Look more closely. You may be missing something..._
