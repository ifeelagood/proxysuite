from core import Proxy
from queue import Queue
import threading
import json

def worker(q, live):


    while not q.empty():

        proxy_address = q.get()
        p = Proxy(proxy_address)
        if p.check():   
            p_dict = p.return_dict()
            print(f"[LIVE] {p_dict['address']}")
            live.append(p_dict)

        q.task_done()



def check_all(proxy_list, thread_num=1000):

    live = []

    q = Queue()

    for p in proxy_list:
        q.put(p)

    threads = []

    for i in range(thread_num):
        threads.append(threading.Thread(target=worker, args=(q,live)))

    for x in threads:
        x.start()

    for x in threads:
        x.join()

    return live