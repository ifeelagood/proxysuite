#!/usr/bin/python3

# README
# to get up to date list -> http://www.proxydb.net/donate

class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):
		
		self.types = types
		self.exceptions = []
		self.name = "ProxyDB"


	def grab_all(self):

		grabbed = [line.rstrip('\n') for line in open('data/proxydb.txt', 'r').readlines()]

		return grabbed