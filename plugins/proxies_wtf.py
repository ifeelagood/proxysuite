#!/usr/bin/python3

import requests
# import re
# import json
from bs4 import BeautifulSoup

class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):

		self.types = types
		self.exceptions = []

	def grab_all(self):

		scraped_proxies = []

		url = "https://proxies.wtf/"

		r = requests.get(url)
		r.raise_for_status()

		soup = BeautifulSoup(r.text, 'html.parser')

		pres = [pre.contents[0] for pre in soup.find_all('pre')]


		http_raw = pres[0].split('\n')
		socks4_raw = pres[1].split('\n')
		socks5_raw = pres[2].split('\n')

		http_proxies = [f"http://{p}" for p in http_raw]
		socks4_proxies = [f"socks4://{p}" for p in socks4_raw]
		socks5_proxies = [f"socks5://{p}" for p in socks5_raw]

		scraped_proxies = http_proxies + socks4_proxies + socks5_proxies

		dupes_removed = []
		dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

		return dupes_removed

if __name__ == '__main__':

	g = Grabber()
	print(g.grab_all())