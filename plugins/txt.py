#!/usr/bin/python3

import requests
import sys

sys.path.append('../')

from data import sources

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        
        self.sources = dict(http=sources.HTTP,socks4=sources.SOCKS4, socks5=sources.SOCKS5)
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

