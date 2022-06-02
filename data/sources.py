#!/usr/bin/python3

import pathlib

# need additional parsing
# 'http://www.xreactorproxy.cf-soft.in/https.php'
# 'http://www.xreactorproxy.cf-soft.in/socks4.php'
# 'http://www.xreactorproxy.cf-soft.in/socks5.php'


def load_source(filename):

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    return lines


HTTP_PATH   = pathlib.Path("data/sources/http.txt")
SOCKS4_PATH = pathlib.Path("data/sources/socks4.txt")
SOCKS5_PATH = pathlib.Path("data/sources/socks5.txt")

HTTP    = load_source(HTTP_PATH)
SOCKS4  = load_source(SOCKS4_PATH)
SOCKS5  = load_source(SOCKS5_PATH)

ALL = HTTP + SOCKS4 + SOCKS5

SOURCE_DICT = {'http': HTTP, 'socks4': SOCKS4, 'socks5': SOCKS5}
