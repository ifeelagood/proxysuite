#!/usr/bin/python3

import requests
# import re
# import json
# from bs4 import BeautifulSoup

class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):

		self.types = types
		self.exceptions = []

	def grab_all(self):

		scraped_proxies = []

		r = requests.get("https://cyber-hub.pw/proxy.txt")
		r.raise_for_status()
		scraped_proxies = r.text

		dupes_removed = []
		dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

		return dupes_removed


if __name__ == '__main__':
	g = Grabber()

	g.grab_all()