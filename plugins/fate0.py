#!/usr/bin/python3

# PLEASE CONSIDER CREATING PULL REQUEST FOR ANY MODULES MADE, IT REALLY DOES HELP!

import requests
# import re
import json
# from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []
        self.name = "fate0's proxy.list"

    def grab_all(self):

        r = requests.get("https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list")
        r.raise_for_status()

        r_json = []

        for r_text in r.text.rstrip('\n').split('\n'):
            r_json.append(json.loads(r_text))

        grabbed = [f"{p['type']}://{p['host']}:{p['port']}" for p in r_json]

        return grabbed
