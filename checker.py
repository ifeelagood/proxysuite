import sys
import threading

import asyncio
import aiohttp
import aiohttp_socks

from bs4 import BeautifulSoup
import json
import re

import tqdm

from proxy import load_proxies, load_proxies_pickle
from arguments import args
from logger import log

try:
    import uvloop
except ImportError:
    log.warning("import uvloop failed. This will significantly decrease performance. Try install if supported on your platform")


class ProgressThread(threading.Thread):

    def __init__(self, event, unchecked, checker_thread):
        threading.Thread.__init__(self)

        self.total = len(unchecked)

        self.pbar = tqdm.tqdm(desc="", total=self.total) # i hate myself

        self.checker_thread = checker_thread

        self.stopped = event


    def run(self):

        while not self.stopped.wait(1):
            self.report_progress()

        self.pbar.close()


    def report_progress(self):

        done = self.checker_thread.completed

        self.pbar.update(done)


class CheckerThread(threading.Thread):

    def __init__(self, proxies):
        threading.Thread.__init__(self)

        self.completed = 0
        self.active = 0

        if "uvloop" in sys.modules:
            self.loop = uvloop.new_event_loop()
        else:
            self.loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self.loop)

        self.tasks = [asyncio.ensure_future(self.check(p)) for p in proxies]

        log.debug("Created tasks")


    def start(self):

        log.debug("starting async check")
        self.loop.run_until_complete(asyncio.wait(self.tasks))


    async def get(self, session, url):

        try:
            async with session.get(url) as resp:
                return await resp.text()

        except Exception as e:
            return None


    async def check(self, proxy):

        if self.active > args.connection_limit:
            while self.active > args.connection_limit:
                await asyncio.sleep(5) # check every 5 seconds to see if space is available

        self.active += 1

        http_url = 'http://api.ipify.org'
        ssl_url = 'https://api.ipify.org'


        proxy_connector = aiohttp_socks.ProxyConnector.from_url(proxy.address)
        session = aiohttp.ClientSession(connector=proxy_connector, timeout=aiohttp.ClientTimeout(total=args.timeout, sock_connect=args.timeout))

        if await self.get(session, http_url) == proxy.host:
            proxy.http = True
        else:
            proxy.http = False

        if await self.get(session, ssl_url):
            proxy.ssl = True
        else:
            proxy.ssl = False


        # evaluate
        if proxy.ssl or proxy.http:
            proxy.working = True
            log.info(f"[LIVE] {proxy}")
        else:
            log.debug(f"[DEAD] {proxy}")
            proxy.working = False


        if not args.basic and proxy.ssl:

            # TODO fixme

            r = await self.get(session, f"https://scamalytics.com/ip/{proxy.host}")

            if r:
                soup = BeautifulSoup(r, 'html.parser')
                fraud_score_string = soup.find("div", {"class": "score"}).contents[0]
                fraud_score = int(re.search(r'(?<=Fraud Score: ).*', fraud_score_string)[0])

                proxy.fraud_score = fraud_score

            r = await self.get(session, f"https://ipapi.co/{proxy.host}/json/")

            if r:
                whois = json.loads(r.text)

                proxy.country_code = whois['country_code']
                proxy.location = (whois['latitude'], whois['longitude'])

        await session.close()

        self.active -= 1
        self.completed += 1

        return proxy


def check_all():

    if args.pickle:
        log.debug("Unpickling...")
        unchecked = load_proxies_pickle(args.input)
    else:
        unchecked = load_proxies(args.input)


    log.debug(f"Loaded {len(unchecked)} proxies from file {args.input}")


    checker_thread = CheckerThread(unchecked)

    if args.progress:
        event = threading.Event()
        progress_thread = ProgressThread(event, unchecked, checker_thread)

        progress_thread.start()
        log.debug("started progress thread")

    checker_thread.start()
    log.debug("started checker thread")

    if args.progress:
        event.set()

        progress_thread.join()

        log.debug("progress thread terminated")

    live = [p for p in unchecked if p.working]

    return live
