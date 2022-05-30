#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pathlib

import requests
import ssl, socket, socks, urllib3 # exceptions

import re
import json

from arguments import args
from logger import log


# constants
global dead_exceptions, http_url, https_url

dead_exceptions = (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, socks.GeneralProxyError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ProxyError, socks.ProxyConnectionError, urllib3.exceptions.ConnectTimeoutError, requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects)
http_url = "http://api.ipify.org"
https_url = "https://api.ipify.org"


class Proxy():

    def __init__(self, address, source=None):

        self.address = address
        self.scheme = urlparse(address).scheme
        
        self.host, self.port = urlparse(address).netloc.split(':')
        self.working = False
        self.borked = False
        self.http = None
        self.ssl = None
        self.country_code = None
        self.fraud_score = None
    
        self.proxy_dict = {'http': self.address, 'https': self.address}

        self.source = source


    def get(self, url):
        
        try:
            r = requests.get(url, proxies=self.proxy_dict, timeout=args.timeout)
            r.raise_for_status()
            return r
        
        except dead_exceptions:
            return False
        
    
    def whois(self):
        
        r = self.get(f"https://ipapi.co/{self.host}/json/")

        if r:
            whois = json.loads(r.text)
            
            self.country_code = whois['country_code']
            self.location = (whois['latitude'], whois['longitude'])
            
            return True
            
        else:
            return False


    def fraud_lookup(self):
        
        r = self.get(f"https://scamalytics.com/ip/{self.host}")

        if r:
            soup = BeautifulSoup(r.text, 'html.parser')
            fraud_score_string = soup.find("div", {"class": "score"}).contents[0]
            fraud_score = int(re.search(r'(?<=Fraud Score: ).*', fraud_score_string)[0])

            self.fraud_score = fraud_score
            
            return True
            
        else:
            return False


    def check(self):

        # HTTP
        if self.get(http_url):
            self.http = True
        else:
            self.http = False


        # SSL
        if self.get(https_url):
            self.ssl = True
        else:
            self.ssl = False
            
        # evaluate
        if self.ssl or self.http:
            self.working = True
        else:
            self.working = False
            return False
        
        
        # if proxy is dead it should not get past this point
        # dont bother with whois etc if not ssl as:
        #    site requires ssl
        #    basically worthless if not ssl

        # advanced check
        if self.ssl and not args.basic:
            
            if not self.whois():
                self.borked = True # passed ssl but failed this
            
            if not self.fraud_lookup():
                self.borked = True # passed ssl but failed this

        return True
    
            
    def return_dict(self):

        self_dict = dict(
                            address = self.address,
                            scheme = self.scheme,
                            host = self.host,
                            port = self.port,
                            http = self.http,
                            ssl = self.ssl,
                            country_code = self.country_code,
                            fraud_score = self.fraud_score
                        )

        return self_dict
    


def dump_proxies(proxies, outfile=pathlib.Path("output/proxyobjects.json")):
    
    proxy_list = [p.return_dict() for p in proxies]

    with open(outfile, 'w') as f:
        json.dump(proxy_list, f)


def load_proxies(infile=pathlib.Path("output/proxyobjects.json")):
    
    temp_proxy_list = {}
    
    with open(infile, 'r') as f:
        json.load(f, temp_proxy_list)
        
    
        
    return proxy_dict