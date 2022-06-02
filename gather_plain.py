#!/usr/bin/python3

import re
import threading

from queue import Queue
import requests

from data import sources
from logger import log


def parse_site(data, url, protocol):

    br_regex = r'<br>'
    newline_regex = r'\n'

    br_count = len(re.findall(br_regex, data))
    newline_count = len(re.findall(newline_regex, data))

    nl = "\n" if newline_count > br_count else "<br>"

    raw = data.rstrip(nl).split(nl)

    scraped = [(f"{protocol}://{ip}", url) for ip in raw]

    return scraped


def scrape_site(url, protocol):

    try:
        r = requests.get(url)
        r.raise_for_status()

    except Exception as e:
        return e

    scraped = parse_site(r.text, url, protocol)

    return scraped


def worker(q, lock, grabbed):

    while q.qsize():

        url, protocol = q.get()

        url_grabbed = scrape_site(url, type)

        if not isinstance(url_grabbed, list):
            log.warning(f"URL '{url}' raised exception while attempting to connect: {url_grabbed}")
            q.task_done()
            continue

        lock.acquire()
        grabbed += url_grabbed
        lock.release()

        log.debug(f"Thread 0 - Scraped from url '{url}' with type '{protocol}'")

        q.task_done()


def grab_all():

    log.debug("Starting gather from plain text sources...")

    grabbed = []

    # list of tuples [(address,source)]

    q = Queue()

    for protocol in ['http', 'socks4', 'socks5']:
        for url in sources.SOURCE_DICT[protocol]:
            q.put((url,protocol))


    thread_num = 32
    threads = []
    lock = threading.Lock()

    for _ in range(thread_num):
        x = threading.Thread(target=worker, args=(q,lock,grabbed))
        threads.append(x)


    for x in threads:
        x.start()

    log.debug("Successfully started plain gather threads")

    for x in threads:
        x.join()

    log.debug("All threads released for plain text sources")

    return grabbed
