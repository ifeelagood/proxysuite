#!/usr/bin/python3

import sys
import struct
import ssl, socket, socks, urllib3 # exceptions

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pathlib

import requests
import urllib3

import re
import json

from arguments import args
from logger import log


# constants
global dead_exceptions, http_url, https_url

dead_exceptions = (urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, socks.GeneralProxyError, urllib3.exceptions.HTTPError)
http_url = "http://api.ipify.org"
https_url = "https://api.ipify.org"



class Proxy():

    def __init__(self, address, source=None):

        urlp = urlparse(address)

        self.address = address
        self.scheme = urlp.scheme

        netloc = urlp.netloc.split(':')

        self.host, self.port = str(netloc[0]), int(netloc[1])

        self.working = False
        self.borked = False
        self.http = None
        self.ssl = None
        self.country_code = None
        self.location = None
        self.fraud_score = None

        self.proxy_dict = None # temporary to keep compatibility with main branch

        self.source = source


    def get(self, url):

        try:
            r = self.pm.request('GET', url)
            if r.status != 200:
                raise urllib3.exceptions.HTTPError("Non-200 HTTP code returned")

            return r

        except dead_exceptions:
            return False


    def whois(self):

        r = self.get(f"https://ipapi.co/{self.host}/json/")

        if r:
            whois = json.loads(r.data.decode('ascii'))

            self.country_code = whois['country_code']
            self.location = (whois['latitude'], whois['longitude'])

            return True

        else:
            return False


    def fraud_lookup(self):

        r = self.get(f"https://scamalytics.com/ip/{self.host}")

        if r:
            soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser')
            fraud_score_string = soup.find("div", {"class": "score"}).contents[0]
            fraud_score = int(re.search(r'(?<=Fraud Score: ).*', fraud_score_string)[0])

            self.fraud_score = fraud_score

            return True

        else:
            return False


    def check(self):

        if self.scheme in ('http', 'https'):
            pm_func = urllib3.ProxyManager
        else:
            pm_func = urllib3.contrib.socks.SOCKSProxyManager

        self.pm = pm_func(self.address) # TODO must set here as when loading, init function not run

        # HTTP
        if self.get(http_url):
            self.http = True
        else:
            self.http = False


        # SSL
        if self.get(https_url):
            self.ssl = True
        else:
            self.ssl = False

        # evaluate
        if self.ssl or self.http:
            self.working = True
        else:
            self.working = False
            del self.pm
            return False


        # if proxy is dead it should not get past this point
        # dont bother with whois etc if not ssl as:
        #    site requires ssl
        #    basically worthless if not ssl

        # advanced check
        if self.ssl and not args.basic:

            if not self.whois():
                self.borked = True # passed ssl but failed this

            if not self.fraud_lookup():
                self.borked = True # passed ssl but failed this

        del self.pm # TODO fixme
        return True


def load_proxy_from_dict(proxy_dict, cls=Proxy):

    actual_init = cls.__init__
    cls.__init__ = lambda *args, **kwargs: None
    instance = cls()
    cls.__init__ = actual_init

    instance.__dict__ = proxy_dict

    return instance



def validate_address(address):

    # validate_regex = r'(http|https|socks4|socks5):\/\/((\d{1,3})(\.\d{1,3}){3}):((\d{1,5}))'
    # regex_valid = bool(re.match(validate_regex, address))

    protocols = ['http', 'https', 'socks4', 'socks5']

    valid = (len(urlparse(address).netloc.split(':')) == 2) and (urlparse(address).scheme in protocols)

    return valid


def dump_proxies(proxies, outfile=pathlib.Path("output/proxyobjects.json")):

    proxy_list = [p.__dict__ for p in proxies]

    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(proxy_list, f)


def load_proxies(infile=pathlib.Path("output/proxyobjects.json")):

    with open(infile, 'r', encoding='utf-8') as f:
        proxy_list_raw = json.load(f)

    proxy_list = []
    for p_dict in proxy_list_raw:
        p = load_proxy_from_dict(p_dict)
        proxy_list.append(p)

    return proxy_list


def construct_object_list(address_list, sourcename):

    object_list = [Proxy(address, sourcename) for address in address_list]

    return object_list


def raw_to_objects(address_list, dedupe=True, exclusive_dedupe=False, validate=True):

    # exclusive dedupe: removes duplicates if source is the same. e.g. (a1, s1) and (a1, s1) are dupes, (a1, s1) and (a1, s2) are not
    # dedupe: removes duplicates which share the same address

    deduped_address_list = address_list

    included_address_list = []

    if exclusive_dedupe:
        for address_tuple in address_list:
            if address_tuple in included_address_list:
                deduped_address_list.remove(address_tuple)
            else:
                included_address_list.append(address_tuple)

    elif dedupe:
        for address_tuple in address_list:
            address, source = address_tuple
            if address in included_address_list:
                deduped_address_list.remove(address_tuple)
            else:
                included_address_list.append(address)


    # validate data
    validated_address_list = deduped_address_list

    if validate:
        for address, sourcename in deduped_address_list:
            if not validate_address(address):
                log.warning(f"Removed invalid address '{address}' from source '{sourcename}'")
                validated_address_list.remove(address)

    object_list = construct_object_list(validated_address_list, sourcename)

    return object_list
