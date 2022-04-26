#!/usr/bin/python3

import requests

class Grabber():

    def __init__(self, source_dict, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.sources = source_dict
        self.exceptions = {}


    def scrape_site(self, url, type):

        try:
            r = requests.get(url)
            r.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            self.exceptions[url] = e
            return []

        src = r.text.strip()

        scraped = [f"{type}://{ip}" for ip in src.split()]
        return scraped

    def grab_all(self):

        scraped_proxies = []

        for protocol in self.types:
            for url in self.sources[protocol]:
                scraped_proxies += self.scrape_site(url, protocol)

        dupes_removed = []
        dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

        return dupes_removed

