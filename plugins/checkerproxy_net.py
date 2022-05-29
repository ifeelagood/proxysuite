#!/usr/bin/python3

import requests
import datetime
import json

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = {}
        self.proxy_type_dict = {1: 'http',
                    2: 'http',
                    3: 'socks4',
                    4: 'socks5'}
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

        scraped_proxies = []
        base_url = "https://checkerproxy.net/api/archive/"

        r = requests.get(base_url)
        r.raise_for_status()

        archive_dict = json.loads(r.text)

        for archive in archive_dict:
            url_date = archive['date']
            scraped_proxies += self.scrape_site(base_url + url_date)

        dupes_removed = []
        dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

        return dupes_removed
