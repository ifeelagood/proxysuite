#!/usr/bin/python3

import requests
# import re
# import json
from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []
        self.name = "cyberhub.pw"

    def grab_all(self):

        grabbed = []

        r = requests.get("https://cyber-hub.pw/proxy.txt")
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        for address in soup.text.rstrip('\n').split('\n'):
            for protocol in self.types:
                grabbed.append(f"{protocol}://{address}")
        

        return grabbed