# AfterImage
## _Evading traditional IOC blocking_

[![N|Solid](https://www.python.org/static/community_logos/python-powered-w-200x80.png)](https://www.python.org/)

AfterImage is a tool that provides anti-forensics capabilities in network-based web attacks. The solution is a proxy-based interceptor that collects attacks and assigns proxies to direct the traffic.

## Features

- Automated web-scraping functionality for discovery of usable web proxies
- Easy to use Web Graphical User Interface
- Local and Remote setup
- Geovisualization of web proxies
- Proxy hopping to bypass defences



## Tech

AfterImage uses a number of open source projects to work properly:

- Python Flask
- Python Threading
- Python Sockets
- Beautiful Soup Web Scraper
- IP Geolocator API
- Bootstrap
- jQuery
- Leaflet.js

## Installation

AfterImage was developed and tested on Python 3.9>.
Create a virtual environment and install the dependencies and run.

```cmd
# Enter AfterImage directory
cd AfterImage

# Create and enter virtual environment
python -m venv virtualenv

# Windows
.\virtualenv\Scripts\activate

# Linux
source ./virtualenv/bin/activate

# Install requirements
pip install -r requirements.txt

# Start AfterImage
python main.py
```
## Usage
AfterImage listens on port 12345 for receiving payloads.

The test scripts below can be used to test AfterImage. 
- The test script "test_without_afterimage.py" in the test folder folder is used to show that the IP returned by an API is the same as our public address.
- While the test script "test_with_afterimage.py" in the test folder folder is used to show that the IP returned by an API is the same as an assigned proxy by AfterImage instead of our public address.

Alternatively, Burp Suite can also be used for testing.
```cmd
# Sending of test payload
python test_with_afterimage.py

# Confirm the attack
1. Access the web console at: http://127.0.0.1:5000
2. Select the tab "Pending" on the left
3. Click on confirm for the attack
4. Wait for response from target and proxy
```
## Result
![AfterImage Result](/images/full_view.png?raw=true)



