#!/usr/bin/python3

import os

from arguments import args
from logger import log, verify_logger_args

import proxy
import checker
import gather


def checker_runner():

    checked = checker.check_all()
    log.debug("check completed. attempting to write to file...")

    if args.pickle:
        log.debug("Pickling...")
        proxy.dump_proxies_pickle(checked, args.output)
    else:
        proxy.dump_proxies(checked, args.output)

    log.info(f"Written output of check to {args.output}")

    proxy.dump_to_lists(checked, "live")

    log.info("Written output of check to plain text files")


def gather_runner():

    # gathered = plugins.__init__.__gather_all__(args, log)
    gathered = gather.gather_all()
    log.debug("Gather completed. attempting to write to file...")

    if args.pickle:
        log.debug("Pickling...")
        proxy.dump_proxies_pickle(gathered, args.output)
    else:
        proxy.dump_proxies(gathered, args.output)

    log.info(f"Written output of gather to {args.output}")

    proxy.dump_to_lists(gathered, "scraped")

    log.info("Written output of gather to plain text files")


def create_output_dirs():

    f = lambda p : os.mkdir(p) if not os.path.exists(p) else None

    output_dirs = ["output", "output/raw"]

    for p in output_dirs:
        if f(p):
            log.info(f"Created missing directory '{p}'")

    # yes, os.makedirs is faster. fuck you


def clear_log():

    if not args.append_log:
        with open(args.log_path, 'w', encoding='utf-8') as f:
            f.truncate()
            log.debug(f"Cleared log file at {args.log_path}")
    else:
        log.info(f"Appending to current log, {args.log_path} not cleared")


if __name__ == '__main__':

    verify_logger_args()

    clear_log()

    create_output_dirs()

    if args.action == 'check':
        log.info("Starting Check...")
        checker_runner()


    if args.action == 'gather':
        log.info("Starting Gather...")
        gather_runner()

    log.info("Completed all tasks! Goodbye!")
