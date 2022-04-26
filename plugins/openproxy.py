#!/usr/bin/python3

import requests
import re
import json
from bs4 import BeautifulSoup

# i absolutely fucking despise regex for grabbing proxies, but it might have to make do

class Grabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        self.exceptions = []
        self.proxy_regex = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{2,5}'
        self.data_regex = r'(?<=data:\[).*(?=\],fetch)'
        self.proto_regex = r'(?<=protocols:).*(?=,anons)'

    def scrape_site(self, url):

        scraped = []

        r = requests.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'html.parser')

        # our father in heaven; hallowed be thy name
        js_raw = soup.body.find_all('script')[0].contents[0]
        protocols_str = re.search(self.proto_regex, js_raw)[0]

        schemes = json.loads(protocols_str) # TODO find out whether http vs https really makes a difference
        scheme = schemes[0]

        # thy kindom come, thy will be done
        data_str = re.search(self.data_regex, js_raw)[0]
        scraped_ips = re.findall(self.proxy_regex, data_str)

        scraped = [f"{scheme}://{proxy}" for proxy in scraped_ips if proxy not in scraped]

        return scraped

    def grab_all(self):

        scraped_proxies = []

        base_url = 'https://openproxy.space/list/'

        for scheme in self.types:
            scraped_proxies += self.scrape_site(base_url+scheme)

        dupes_removed = []
        dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

        return dupes_removed


