#!/usr/bin/python3

import re

import requests

import selenium.webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import time

class Grabber():

    def __init__(self):

        self.name = "spys_one"

        webdriver_options = selenium.webdriver.chrome.options.Options()
        # webdriver_options.add_argument("--headless")

        self.webdriver = selenium.webdriver.Chrome(options=webdriver_options)

    def scrape_page(self):

        self.webdriver.get("https://spys.one/en/free-proxy-list/")

        # wait for page load
        wait = WebDriverWait(self.webdriver, 30)
        _ = wait.until(ec.visibility_of_element_located((By.XPATH, "//html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[3]/td[1]/font")))

        showcount_select = Select(self.webdriver.find_element(By.XPATH, "//*[@id='xpp']"))

        showcount_select.select_by_visible_text('500')

        _ = wait.until(ec.visibility_of_element_located((By.XPATH, "//html/body/table[2]/tbody/tr[4]/td/table/tbody/tr[3]/td[1]/font")))

        ssl_select = Select(self.webdriver.find_element(By.XPATH, "//*[@id='xf1']"))
        ssl_select.select_by_value('1') # ssl on

        _ = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[4]/td/table/tbody")))

        time.sleep(2)

        soup = BeautifulSoup(self.webdriver.page_source, "html.parser")

        tbody = soup.find("td", {"colspan": "10"}).table.tbody

        for tr in tbody.find_all('tr')[1:]:

            tds = tr.find_all('td')

            combo = tds[0].contents()
            protocol = tds[1].a.contents()[0]

            print(combo, protocol)


        return None


    def grab_all(self):

        self.scrape_page()

if __name__ == '__main__':
    g = Grabber()
    grabbed = g.grab_all()