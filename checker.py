from core import Proxy
from queue import Queue
import threading
import json


def worker(q, live, args):

    while not q.empty():

        proxy_address = q.get()
        p = Proxy(proxy_address)
        if p.check(args.timeout):   
            p_dict = p.return_dict()
            print(f"[LIVE] {p_dict['address']}")
            live.append(p_dict)

        q.task_done()


def basic_worker(q, live, args):
    
    while not q.empty():

        proxy_address = q.get()
        p = Proxy(proxy_address)
        if p.check_basic(args.timeout):   
            p_dict = p.return_dict()
            print(f"[LIVE] {p_dict['address']}")
            live.append(p_dict)

        q.task_done()


def check_all(args):

    with open(args.input, 'r') as f:
        unchecked = [line.rstrip('\n') for line in f.readlines()]

    live = []

    q = Queue()

    for p in unchecked:
        q.put(p)

    threads = []

    worker_target = worker if not args.basic else basic_worker

    for i in range(args.threads):
        threads.append(threading.Thread(target=worker_target, args=(q,live, args)))

    for x in threads:
        x.start()

    for x in threads:
        x.join()

    return live
