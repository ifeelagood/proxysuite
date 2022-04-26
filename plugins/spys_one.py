#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent

# xx0: an md5 hash in the format \d584457
# xpp: how many to show (500 proxies = 5)
# xf5: proxy type (2=socks, 1=http)
class Grabber():

	def __init__(self, types=['http', 'socks4', 'socks5']):

		self.types = types
		self.exceptions = {}
		self.headers = {'user-agent': UserAgent().get_random_user_agent()}

	def scrape_site(self, type):

		scraped = []

		url = "https://spys.one/en/free-proxy-list/"

		s = requests.Session()
		s.headers.update(self.headers)

		r = s.get(url)
		r.raise_for_status()

		soup = BeautifulSoup(r.text, 'html.parser')

		# i have zero clue what xx0 is actually for. its an md5 hash with a random integer
		# proceeded by 584457. e.g. 7584457

		xx0 = soup.find('input', {'name': 'xx0'})['value']
		xf5 = 1 if type == 'http' else 2

		request_data = dict(xx0=xx0, xpp=5, xf1=0, xf2=0, xf4=0, xf5=xf5)

		r = s.post(url, data=request_data)
		r.raise_for_status()

		soup = BeautifulSoup(r.text, 'html.parser')

		# tr classes:
		# spy1xx, spy1x
		rows_1 = soup.find_all('tr', {'class': 'spy1x'})
		rows_2 = soup.find_all('tr', {'class': 'spy1xx'})
		rows = rows_1 + rows_2
		del rows[0]

		obsfuscation_string = soup.body.find('script', {'type': 'text/javascript'}).contents[0].rstrip(';')


		# dont ask; just watch
		obs_dict = {}
		for line in obsfuscation_string.split(';'):
			key, value = line.split('=')
			if '^' in value:
				new_value = value.split('^')[0]
				obs_dict[key] = new_value

		obs_regex = r'[a-z0-9]{6}\^[a-z0-9]{4}'

		for row in rows:
			cols = row.find_all('td')

			scheme = cols[1].a.font.contents[0].lower()
			ip = cols[0].font.contents[0]
			port = ''


			for x in re.findall(obs_regex, str(cols[0].font.script)):
				obs_num = x.split('^')[0]
				port += obs_dict[obs_num]
			address = f"{scheme}://{ip}:{port}"
			scraped.append(address)

		return scraped

	def grab_all(self):

		scraped_http = self.scrape_site('http')
		scraped_socks = self.scrape_site('socks')
		grabbed = scraped_http + scraped_socks

		dupes_removed = []
		dupes_removed = [proxy for proxy in grabbed if proxy not in dupes_removed]
		return dupes_removed

