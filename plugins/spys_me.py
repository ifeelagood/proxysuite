#!/usr/bin/python3

import requests

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

		src = r.text.strip()

		scraped = []

		lines = src.split('\n')

		for i,line in enumerate(lines):
			if 5 < i < (len(lines) - 2):
				scraped.append(f"{type}://{line.split()[0]}")

		return scraped


	def grab_all(self):

		scraped_proxies = []

		socks_url = 'https://spys.me/socks.txt'
		http_url = 'https://spys.me/proxy.txt'

		http_scraped = self.scrape_site(http_url, 'http')
		socks_scraped = self.scrape_site(socks_url, 'socks4') + self.scrape_site(socks_url, 'socks5')

		grabbed = http_scraped + socks_scraped

		dupes_removed = []
		dupes_removed = [proxy for proxy in grabbed if proxy not in dupes_removed]

		return dupes_removed

