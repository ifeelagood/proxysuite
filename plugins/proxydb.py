#!/usr/bin/python3

# README
# to get up to date list -> http://www.proxydb.net/donate
class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):
		
		self.types = types
		self.exceptions = []


	def grab_all(self):

		scraped_proxies = [line.rstrip('\n') for line in open('data/proxydb.txt', 'r').readlines()]

		dupes_removed = []
		dupes_removed = [proxy for proxy in scraped_proxies if proxy not in dupes_removed]

		return dupes_removed