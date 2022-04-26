#!/usr/bin/python3

import requests
# import re
# import json
# from bs4 import BeautifulSoup

class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):

		self.types = types
		self.exceptions = []

	def scrape_site(self, url, type):

		scraped = []

		# stuff here

		return scraped

	def grab_all(self):

		scraped_proxies = []

		# and here

		dupes_removed = []
		dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

		return dupes_removed
