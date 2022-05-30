#!/usr/bin/python3

# PLEASE CONSIDER CREATING PULL REQUEST FOR ANY MODULES MADE, IT REALLY DOES HELP!

import requests
# import re
# import json
# from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []
  
        self.name = "template"
        self.url = ""


    def grab_all(self):

        grabbed = []

        return grabbed
