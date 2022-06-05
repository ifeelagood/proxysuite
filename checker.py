import threading
import time

from queue import Queue

from proxy import Proxy, load_proxies
from arguments import args
from logger import log


import asyncio
import aiohttp
import aiohttp_socks

import python_socks

def worker(q, lock, live):

    while not q.empty():

        p = q.get()

        if p.check():

            log.info(f"[LIVE] {p.address}")

            lock.acquire()
            live.append(p)
            lock.release()

        else:
            log.debug(f"[DEAD] {p.address}")

        q.task_done()


class ProgressThread(threading.Thread):

    def __init__(self, event, unchecked, checker_thread):
        threading.Thread.__init__(self)

        self.total = len(unchecked)
        self.checker_thread = checker_thread

        self.stopped = event


    def run(self):

        while not self.stopped.wait(10):
            self.report_progress()


    def report_progress(self):

        done = self.checker_thread.completed
        remaining = self.total - done
        progress = done / self.total
        progress_perc = round(progress * 100, 2)

        log.info(f"{progress_perc}%\tChecked: {done} - Remaining: {remaining}")


class CheckerThread(threading.Thread):

    def __init__(self, proxies):
        threading.Thread.__init__(self)

        self.completed = 0
        self.active = 0


        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.check(p)) for p in proxies]

        log.debug("Created tasks. Running")
        loop.run_until_complete(asyncio.wait(tasks))



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
            log.debug(f"[DEAD], {proxy}")
            proxy.working = False


        await session.close()

        self.active -= 1
        self.completed += 1

        return proxy


def check_all():

    unchecked = load_proxies(args.input)
    log.debug(f"Loaded {len(unchecked)} proxies from file {args.input}")


    checker_thread = CheckerThread(unchecked)

    event = threading.Event()
    progress_thread = ProgressThread(event, unchecked, checker_thread)

    checker_thread.start()
    log.debug("started checker thread")

    progress_thread.start()
    log.debug("started progress thread")

    checker_thread.join()
    log.debug("checker thread terminated")

    event.set()

    progress_thread.join()
    log.debug("progress thread terminated")

    live = [p for p in unchecked if p.working]

    return live
