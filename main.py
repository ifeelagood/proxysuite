#!/usr/bin/python3

import os
import json
import pathlib

from arguments import args
from logger import log, verify_logger_args

import checker
import gather
import plugins


def checker_runner():
    
    checked = checker.check_all()
    log.debug("check completed. dumping to json...")

    with open(args.output, 'w') as f:
        json.dump(checked, f)


def gather_runner():
    
    # gathered = plugins.__init__.__gather_all__(args, log)
    gathered = gather.gather_all()
    log.debug(f"gather completed. attempting to write to file")

    if not args.output.parent.exists():
        os.mkdir(args.output.parent)
        log.info(f"Created output directory at {args.output.parents}")

    with open(args.output, 'w') as f:
        for p in gathered:
            f.write(p + '\n')

    log.info(f"Written output of gather to {args.output}")


if __name__ == '__main__':

    verify_logger_args()

    if args.action == 'check':
        checker_runner()
        
    if args.action == 'gather':
        log.info(f"Starting Gather...")
        gather_runner()
        log.info("Done!")