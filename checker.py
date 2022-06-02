import threading

from queue import Queue

from proxy import Proxy, load_proxies
from arguments import args
from logger import log


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

    def __init__(self, event, q, live):
        threading.Thread.__init__(self)

        self.queue = q
        self.live = live
        self.startcount = q.qsize()

        self.stopped = event

    def run(self):
        while not self.stopped.wait(10):
            self.report_progress()

            # call a function

    def report_progress(self):
        live = len(self.live)
        remaining = self.queue.qsize()
        done = self.startcount - remaining
        progress = done / self.startcount
        progress_perc = round(progress * 100, 2)

        log.info(f"{progress_perc}%\tChecked: {done} - Remaining: {remaining} - Live: {live}")


def check_all():

    unchecked = load_proxies(args.input)
    log.debug(f"Loaded proxies from file {args.input}")

    live = []

    q = Queue()

    for p in unchecked:
        q.put(p)


    stop_flag = threading.Event()
    progress_thread = ProgressThread(stop_flag, q, live)
    progress_thread.start()

    log.debug("Started progress monitoring thread")

    lock = threading.Lock()

    threads = [threading.Thread(target=worker, args=(q, lock, live)) for _ in range(args.threads)]

    log.debug("Created checker threads")

    for x in threads:
        x.start()

    log.debug("Started checker threads, joining")

    for x in threads:
        x.join()

    log.debug("Checker threads exited successfully")

    log.debug("Waiting for progress thread to terminate...")

    stop_flag.set()
    progress_thread.join()

    log.debug("Progress thread exited successfully")


    return live
