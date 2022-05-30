import threading
import json

from queue import Queue

from proxy import Proxy, load_proxies
from arguments import args
from logger import log


def worker(q, lock, live):
    
    global reported
    startsize = q.qsize()
    reported = startsize
    
    while not q.empty():
        
        remaining = q.qsize()
        if remaining % 1000 == 0 and remaining != reported:
            
            lock.acquire()
            reported = remaining
            completed = startsize - remaining
            completion_percentage = round((completed / startsize)*100, 2)
            log.info(f"Completed: {completed}, Remaining: {remaining}, Progress: {completion_percentage}%")
            lock.release()

        proxy_address = q.get()
        p = Proxy(proxy_address)
        
        
        if p.check():
            
            log.info(f"[LIVE] {p.address}")
            
            p_dict = p.return_dict()
            
            lock.acquire()
            live.append(p_dict)
            lock.release()

        else:
            log.debug(f"[DEAD] {p.address}")

        q.task_done()




def check_all():

    unchecked = load_proxies(args.input)
    log.debug(f"Loaded proxies from file {args.input}")

    live = []

    q = Queue()

    for p in unchecked:
        q.put(p)

    lock = threading.Lock()
    
    threads = []

    for i in range(args.threads):
        threads.append(threading.Thread(target=worker, args=(q, lock, live)))

    for x in threads:
        x.start()

    for x in threads:
        x.join()

    return live
