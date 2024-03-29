#!/usr/bin/python3

import pickle

import sys
import ssl, socket, socks, urllib3 # exceptions


from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pathlib

import requests

import asyncio
import aiohttp
import aiohttp_socks

import re
import json

from arguments import args
from logger import log


# constants
global dead_exceptions, http_url, https_url

dead_exceptions = (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, socks.GeneralProxyError, requests.exceptions.ChunkedEncodingError, requests.exceptions.ProxyError, socks.ProxyConnectionError, urllib3.exceptions.ConnectTimeoutError, requests.exceptions.SSLError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects)
http_url = "http://api.ipify.org"
https_url = "https://api.ipify.org"



class Proxy():

    def __init__(self, address, source=None):

        self.address = address
        self.scheme = urlparse(address).scheme

        self.host, self.port = urlparse(address).netloc.split(':')
        self.working = False
        self.borked = False
        self.http = None
        self.ssl = None
        self.country_code = None
        self.location = None
        self.fraud_score = None

        self.proxy_dict = None # temp to maintain compat. with old

        self.source = source


    def __str__(self):
        return self.address


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

    netloc = urlparse(address).netloc.split(':')

    valid_netloc = len(netloc) == 2
    valid_scheme = urlparse(address).scheme in protocols

    if valid_netloc:
        valid_port = int(netloc[1]) <= 2**16-1
    else:
        valid_port = False

    # TODO fix this monstrosity

    valid = (valid_netloc and valid_scheme and valid_port)


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
        try:
            p = load_proxy_from_dict(p_dict)
            proxy_list.append(p)
        except Exception():
            log.exception(f"Proxy from file {infile} threw execption while loading. Relevant JSON object: {p_dict}. Printing trace: ")

    return proxy_list


def dump_proxies_pickle(proxies, outfile=pathlib.Path("output/proxyobjects.pkl")):

    with open(outfile, 'wb') as f:
        pickle.dump(proxies, f)


def load_proxies_pickle(infile=pathlib.Path("output/proxyobjects.pkl")):

    with open(infile, 'rb') as f:
        proxy_list = pickle.load(f)

    return proxy_list


def dump_to_lists(object_list, subdirectory):

    all_f = open(f"output/raw/{subdirectory}/all.txt", 'w', encoding='utf-8')
    http_f = open(f"output/raw/{subdirectory}/http.txt", 'w', encoding='utf-8')
    socks4_f = open(f"output/raw/{subdirectory}/socks4.txt", 'w', encoding='utf-8')
    socks5_f = open(f"output/raw/{subdirectory}/socks5.txt", 'w', encoding='utf-8')

    for p in object_list:

        all_f.write(p.address + '\n')

        if p.scheme == 'http':
            http_f.write(p.address + '\n')
        if p.scheme == 'socks4':
            socks4_f.write(p.address + '\n')
        if p.scheme == 'socks5':
            socks5_f.write(p.address + '\n')

    all_f.close()
    http_f.close()
    socks4_f.close()
    socks5_f.close()


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
