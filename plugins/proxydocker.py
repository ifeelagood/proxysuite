#!/usr/bin/python3

import requests
# import re
import json
from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []

        self.name = "proxydocker.com"



    def grab_all(self):

        grabbed = []

        type_dict = {"1": 'http', "2": 'https', "12": 'https', "126": 'https', "3": 'socks4', "4": 'socks5'}

        s = requests.session()
        r = s.get("https://www.proxydocker.com/en/")

        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find("meta", {"name": "_token"})['content'] # i dont know why people even bother at this point.

        for i in range(2):
            form_data = {
                            "token":    token,
                            "country":  "all",
                            "city":     "all",
                            "state":    "all",
                            "port":     "all",
                            "type":     "all",
                            "anonymity":"all",
                            "need":     "all",
                            "page":     str(i+1)
                            }


            r = s.post("https://www.proxydocker.com/en/api/proxylist/", data=form_data)
            r_json = json.loads(r.text)

            grabbed_page = [f"{type_dict[p['type']]}://{p['ip']}:{p['port']}" for p in r_json["proxies"] if p['type'] in type_dict.keys()] # fuck clean code
            grabbed += grabbed_page



        return grabbed
