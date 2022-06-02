#!/usr/bin/python3

import os
import json
import pathlib

from arguments import args
from logger import log, verify_logger_args

import proxy
import checker
import gather
import plugins


def checker_runner():

    checked = checker.check_all()
    log.debug("check completed. attempting to write to file...")

    proxy.dump_proxies(checked, args.output)

    log.info(f"Written output of check to {args.output}")


def gather_runner():

    # gathered = plugins.__init__.__gather_all__(args, log)
    gathered = gather.gather_all()
    log.debug(f"gather completed. attempting to write to file...")


    proxy.dump_proxies(gathered, args.output)

    log.info(f"Written output of gather to {args.output}")


if __name__ == '__main__':

    verify_logger_args()

    if args.action == 'check':
        checker_runner()

    if args.action == 'gather':
        log.info(f"Starting Gather...")
        gather_runner()
        log.info("Done!")