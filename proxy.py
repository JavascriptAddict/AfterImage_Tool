import requests
import re
from random import randint
from bs4 import BeautifulSoup
from log import Logger
from locater import *

class Proxy:
    '''Proxy class for object store'''
    def __init__(self, data):
        '''Init function'''
        self.connState = True
        self.ip = data[0]
        self.port = data[1]
        self.countryCode = data[2]
        self.country = data[3]
        self.https = data[6]
        self.timeLastChecked = data[7]
        self.lat = 0.0
        self.lng = 0.0
    
class Proxies:
    '''Proxies class to store and control proxies''' 
    def __init__(self):
        '''Init function'''
        self.proxyList = list()
        self.proxyURL = "https://free-proxy-list.net/"
        self.logger = Logger()

    def update(self):
        '''Update list of proxy by scraping'''
        self.logger.out("Scraping for proxies...")
        page = requests.get(self.proxyURL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="fpl-list")
        proxyElements = results.find_all("tr")
        for index, proxyElement in enumerate(proxyElements):
            if index < 1:
                continue
            regex = "<td[^>]*>([^<]+)</td>"
            pattern = re.compile(regex)
            data = re.findall(pattern, proxyElement.prettify())
            data = [x.strip(' \n') for x in data]
            # Limited it to 50 so that we don't accidently DOS
            if index == 50:
                break
            self.logger.out("Adding proxy: {}".format(data[0]))
            self.addProxy(data)

    def addProxy(self, data):
        '''Add new proxy object based on update'''
        newProxy = Proxy(data)
        updatedProxy = addLocation(newProxy)
        self.proxyList.append(newProxy)
    
    def getProxy(self):
        '''Return random proxy if status available'''
        activeProxy = False
        chosenIndex = 0
        while not activeProxy:
            index = randint(0, len(self.proxyList) - 1)
            if self.proxyList[index].connState:
                activeProxy = True
                chosenIndex = index
                break 
        return self.proxyList[chosenIndex]
    
    def updateProxyConn(self, proxy):
        for proxyObject in self.proxyList:
            if proxyObject.ip == proxy.ip:
                proxyObject.connState =  False



            



