#!/usr/bin/python3

import threading
import sys
import requests

from queue import Queue

sys.path.append('../')

from data import sources
from proxy import Proxy
from logger import log

class TXTGrabber():

    def __init__(self, types=['http', 'socks4', 'socks5']):

        self.types = types
        
        self.sources = dict(http=sources.HTTP,socks4=sources.SOCKS4, socks5=sources.SOCKS5)
        self.exceptions = {}
        
        # self.name = "" 
        # change name depending on source


    def scrape_site(self, url, type):

        try:
            r = requests.get(url)
            r.raise_for_status()

        except Exception as e:
            return e

        src = r.text.strip()

        scraped = [(f"{type}://{ip}", url) for ip in src.split()]
        
        return scraped


    def worker(self, q, lock, grabbed, i):
        
        while q.qsize():
            
            url, protocol = q.get()
            
            url_grabbed = self.scrape_site(url, type)
            
            if type(url_grabbed) != list:
                log.warn(f"URL '{url}' raised exception while attempting to connect: {url_grabbed}")
                q.task_done()
                continue
            
            lock.acquire()
            grabbed += url_grabbed
            lock.release()
            
            log.debug(f"Thread 0 - Scraped from url '{url}' with type '{protocol}'")

            q.task_done()


    def grab_all(self):

        log.debug("Starting gather from plain text sources...")

        grabbed = []

        # list of tuples [(address,source)]

        q = Queue()
        lock = threading.Lock()

        for protocol in self.types:
            for url in self.sources[protocol]:
                q.put((url,protocol))
                grabbed += self.scrape_site(url, protocol)

        thread_num = 16
        threads = []
        
        for i in range(thread_num):
            x = threading.Thread(target=self.worker, args=(q,lock,grabbed,i))
            threads.append(x)
            log.debug(f"Created thread {i}")    
        
        for x in threads:
            x.start()
            
        for x in threads:
            x.join()
            
        log.debug("All threads released for plain text sources")
        
        return grabbed

