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

    proxy.dump_proxies(checked, args.output)

    log.info(f"Written output of check to {args.output}")

    proxy.dump_to_lists(checked)

    log.info(f"Written output of check to plain text files")


def gather_runner():

    # gathered = plugins.__init__.__gather_all__(args, log)
    gathered = gather.gather_all()
    log.debug(f"gather completed. attempting to write to file...")


    proxy.dump_proxies(gathered, args.output)

    log.info(f"Written output of gather to {args.output}")


def create_output_dirs():

    f = lambda p : os.mkdir(p) if not os.path.exists(p) else None

    output_dirs = ["output", "output/raw"]

    for p in output_dirs:
        f(p)
        log.info(f"Created missing directory '{p}'")

    # yes, os.makedirs is faster. fuck you


if __name__ == '__main__':

    verify_logger_args()

    create_output_dirs()

    if args.action == 'check':
        log.info("Starting Check...")
        checker_runner()


    if args.action == 'gather':
        log.info("Starting Gather...")
        gather_runner()

    log.info("Completed all tasks! Goodbye!")
