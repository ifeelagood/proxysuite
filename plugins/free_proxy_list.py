#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = {}

    def scrape_site(self, url, type):

        try:
            r = requests.get(url)
            r.raise_for_status()

        except requests.exceptions.ConnectionError:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', {'class': 'table table-striped table-bordered'})

        scraped = []

        for tr in table.find_all('tr'):
            fields = tr.find_all('td')
            if len(fields):
                scraped.append(f"{type}://{fields[0].contents[0]}:{fields[1].contents[0]}")
        return scraped

    def grab_all(self):

        scraped_proxies = []

        http_url = 'https://free-proxy-list.net/'
        socks_url = 'https://www.socks-proxy.net/'

        http_scraped = self.scrape_site(http_url, 'http')
        socks_scraped = self.scrape_site(socks_url, 'socks4') + self.scrape_site(socks_url, 'socks5')

        grabbed = http_scraped + socks_scraped

        return grabbed

