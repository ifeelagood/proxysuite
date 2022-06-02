#!/usr/bin/python3

import json
import requests


class Grabber():

    def __init__(self):

        self.types = ['http', 'socks4', 'socks5']
        self.exceptions = {}
        self.proxy_type_dict = {1: 'http',
                    2: 'http',
                    3: 'socks4',
                    4: 'socks5'}

        self.name = "checkerproxy.net"


    def scrape_site(self, url):

        scraped = []

        try:
            r = requests.get(url)
            r.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            self.exceptions[url] = e
            return []

        proxy_dict_lst = json.loads(r.text)

        scraped = [f"{self.proxy_type_dict[proxy['type']]}://{proxy['addr']}" for proxy in proxy_dict_lst]

        return scraped


    def grab_all(self):

        grabbed = []
        base_url = "https://checkerproxy.net/api/archive/"

        r = requests.get(base_url)
        r.raise_for_status()

        archive_dict = json.loads(r.text)

        for archive in archive_dict:
            url_date = archive['date']
            grabbed += self.scrape_site(base_url + url_date)

        return grabbed