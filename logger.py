#!/usr/bin/python3

import logging

from arguments import args

# TODO fix global inside module


def init_logger(name='proxysuite'):

    log = logging.getLogger(name)

    chformatter = logging.Formatter('[%(levelname)s] %(message)s')
    fhformatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(message)s')


    enable_console = not (args.silent or args.quiet)
    enable_filestream = not args.silent


    log.setLevel(args.log_level * 10)


    if enable_filestream:
        fh = logging.FileHandler(args.log_path)
        fh.setLevel(args.file_log_level * 10) # logging.DEBUG = 10, logging.INFO = 20....
        fh.setFormatter(fhformatter)
        log.addHandler(fh)


    if enable_console:
        ch = logging.StreamHandler()
        ch.setLevel(args.log_level * 10)
        ch.setFormatter(chformatter)
        log.addHandler(ch)

    return log


def verify_logger_args():

    invalid_level = lambda x : not 1 <= x <= 5

    if invalid_level(args.log_level):
        message = f"Invalid value '{args.log_level}' for log level parameter --log-level,-p."
        raise ValueError(message)


    if invalid_level(args.file_log_level):
        message = f"Invalid value '{args.file_log_level}' for log level parameter --file-log-level."
        raise ValueError(message)


global log
log = init_logger()
