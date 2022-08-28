#!/usr/bin/python3

# import re
import itertools
import json

import requests
from bs4 import BeautifulSoup

import tqdm

class Grabber():

    def __init__(self):

        self.name = "proxydocker.com"

    def scape_page(self, session, form_data):

        protocol_map = {"1": 'http', "2": 'https', "12": 'https', "126": 'https', "3": 'socks4', "4": 'socks5'}


        valid_response = False
        while not valid_response:
            try:
                r = session.post("https://www.proxydocker.com/en/api/proxylist/", data=form_data)
                r.raise_for_status()
                r_json = json.loads(r.text)

            except:
                print("problem with the server! please switch ips!")
                _ = input("waiting on user input...")
                continue

            valid_response = True



        page_scraped = []

        for proxy in r_json["proxies"]:
            host, port = proxy["ip"], proxy["port"]

            protocol = proxy["type"]

            if protocol not in protocol_map.keys():
                continue

            address = f"{protocol}://{host}:{port}"

            page_scraped.append(address)

        return page_scraped


    def create_form_data(self, token, combination, fields):

        assert len(combination) == len(fields)

        form_data = {
            "token":		token,
            "country":		"all",
            "city":			"all",
            "state":		"all",
            "port":			"all",
            "type":			"all",
            "anonymity":	"all",
            "need":			"all",
            "page":			"1"
        }

        fields_combination = zip(fields, combination)

        for field, field_value in fields_combination:
            form_data[field] = field_value

        return form_data


    def grab_all(self):

        scraped = set()

        s = requests.session()

        r = s.get("https://proxydocker.com/en/")
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        token = soup.find("meta", {"name": "_token"})['content'] # i dont know why people even bother at this point.


        with open("proxydocker.html", 'r', encoding='utf-8') as f:
            html = f.read()


        # html_soup = BeautifulSoup(html, 'html.parser')
        # find_possibles = lambda tag, param, value : [option['value'] for option in html_soup.find(tag, {param: value}).find_all("option")]

        possible_countries=['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia', 'Asia/Pacific Region', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo', 'Congo Democratic', 'Costa Rica', 'Cote Ivoire', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Estonia', 'Ethiopia', 'Europe', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman', 'Pacific Region', 'Pakistan', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Samoa', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Virgin Islands, U.S.', 'Yemen', 'Zambia', 'Zimbabwe']
        possible_types=['http-https', 'https', 'socks', 'socks4', 'socks5']
        possible_ports=['8080', '808', '80', '3128', '8998', '1189', '8123', '8118', '1080', '65000', '53281', '45554', '8888', '8085', '10000', '9000', '8081', '8088', '14', '45454', '13', '24631', '90', '9064', '12', '50', '24632', '25', '443', '38', '15', '9999', '17', '16', '11', '9001', '30', '18', '10', '28', '22', '21', '21320', '9797', '32', '23', '8000', '27', '29', '31']
        possible_anonymity=['ELITE', 'ANONYMOUS', 'TRANSPARENT']

        pages = (1,2)


        combinations = list(itertools.product(possible_types, pages))

        fields = ("type", "page")

        combo_count = len(combinations)


        for i,combination in enumerate(combinations):

            print(list(zip(fields, combination)), len(scraped), f"{i}/{combo_count}", sep='\t')

            combo_form_data = self.create_form_data(token, combination, fields)
            combo_scraped = self.scape_page(s, combo_form_data)

            for address in combo_scraped:
                scraped.add(address)



        scraped = list(scraped)


        return scraped


if __name__ == '__main__':

    g = Grabber()

    grabbed = g.grab_all()

    print(grabbed)
