#!/usr/bin/python3

import requests
# import re
# import json
from bs4 import BeautifulSoup

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []

    def scrape_site(self, url, pagenum):

        scraped = []

        # stuff here

        cookie_dict = {'anonymity': 'all', 'page': str(pagenum)}
        r = requests.get(url, cookies=cookie_dict)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', {'class': 'table table-bordered'}).tbody

        rows = table.find_all('tr')

        for row in rows:
            cols = [col.contents[0] for col in row.contents]

            host = cols[0]
            port = cols[1]
            scheme = cols[2].lower()
            if scheme == 'https':
                scheme = 'http'

            address = f"{scheme}://{host}:{port}"
            scraped.append(address)

        return scraped

    def grab_all(self):

        scraped_proxies = []

        url = 'https://proxyhub.me/'
        # and here

        for i in range(100):
            scraped_proxies += self.scrape_site(url, i+1)

        dupes_removed = []
        dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

        return dupes_removed

if __name__ == '__main__':
    g = Grabber()
    x = g.grab_all()
    print(x)
