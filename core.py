#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import re
import json
import ssl
import socket
import socks
import urllib3

class Proxy():

    def __init__(self, address):

        self.address = address
        self.scheme = urlparse(address).scheme
        self.host, self.port = urlparse(address).netloc.split(':')
        self.working = False
        self.http = None
        self.ssl = None
        self.country_code = None
        self.fraud_score = None


    def check(self):

        proxy_dict = {'http': self.address, 'https': self.address}

        dead_exceptions = (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, socks.GeneralProxyError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ProxyError, socks.ProxyConnectionError, urllib3.exceptions.ConnectTimeoutError, requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects)

        t = 15 # TODO fixme

        # basic http test
        http_url = 'http://api.ipify.org'

        try:
            r = requests.get(http_url, proxies=proxy_dict, timeout=t)
            r.raise_for_status()
            self.http = True

        except dead_exceptions:
            self.http = False


        # ssl test
        https_url = 'https://api.ipify.org'

        try:
            r = requests.get(https_url, proxies=proxy_dict, timeout=t)
            r.raise_for_status()
            self.ssl = True

        except dead_exceptions as e: # TODO find errors specific to proxies where http works but not https
            self.ssl = False

        if (not self.ssl) and (not self.http):
            return False
        else:
            self.working = True

        # if proxy is dead it should not get past this point


        # dont bother with whois etc if not ssl as:
        #     site requires ssl
        #    basically worthless if not ssl

        if self.ssl:

            # whois lookup
            
            whois_url = f"https://ipapi.co/{self.host}/json/"
            
            try:
                r = requests.get(whois_url, proxies=proxy_dict, timeout=t)
                r.raise_for_status()

                whois = json.loads(r.text)

                self.country_code = whois['country_code']
                self.location = (whois['latitude'], whois['longitude'])

            except dead_exceptions:
                self.ssl = False
                return True
            # fraud score lookup

            fraud_url = f"https://scamalytics.com/ip/{self.host}"


            try:
                r = requests.get(fraud_url, proxies=proxy_dict, timeout=t)
                r.raise_for_status()

                #latencies.append(r.elapsed)

                soup = BeautifulSoup(r.text, 'html.parser')
                fraud_score_string = soup.find("div", {"class": "score"}).contents[0]
                fraud_score = int(re.search(r'(?<=Fraud Score: ).*', fraud_score_string)[0])

                self.fraud_score = fraud_score
            except dead_exceptions:
                self.ssl = False
                return True


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