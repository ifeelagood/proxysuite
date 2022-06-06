#!/usr/bin/python3

import pathlib
import argparse

global args


log_help_string = "Supported values: 1=DEBUG, 2=INFO, 3=WARNING, 4=ERROR, 5=CRITICAL"


parser = argparse.ArgumentParser(description='Scrape and check proxies.')
parser.add_argument('action', choices=['check', 'gather'], help="Check proxies from file and write to file/Gather proxies from plugins and write to file")

# IO
parser.add_argument('-o', '--output', type=pathlib.Path, default=None, metavar="OUTPUT_PATH", help="Specify file path to be written to")
parser.add_argument('-i', '--input', type=pathlib.Path, default=None, metavar="INPUT_PATH", help="Specify file path to be read from")
parser.add_argument('-p', '--pickle', action='store_true', default=False, help="Use pickle (object to datastream) to dump/load IO. Reduces file size. WARNING: NOT SECURE. DO NOT LOAD ANYTHING YOU DIDN'T CREATE YOURSELF")

# checker
parser.add_argument('-b', '--basic', action='store_true', default=False, help="Use only HTTP and SSL test when checking proxies") # couldnt get py3.9 argparse.BooleanOptionalAction to work TODO
parser.add_argument('-L', '--connection-limit', type=int, default=1024, metavar="LIMIT", help="Specify limit of open sessions. helps with 'Too many open files'")
parser.add_argument('-t', '--timeout', type=int, default=15, metavar="SECONDS", help="Specify request timeout in seconds when checking proxies")

# logging
parser.add_argument('-c', '--log-level', type=int, default=2, help="Specify log level for console/stdout " + log_help_string) # INFO
parser.add_argument('-f', '--file-log-level', type=int, default=1, help="Specify log level for log file " + log_help_string) # DEBUG
parser.add_argument('--log-path', type=pathlib.Path, default=pathlib.Path("proxysuite.log"), metavar="LOG_PATH", help="Specify file path for log")

parser.add_argument('-q', '--quiet', action='store_true', default=False, help="Disable console/stdout logging") # supress stdout
parser.add_argument('-s', '--silent', action='store_true', default=False, help="Disable logging") # supress stdout and log

parser.add_argument('-A', '--append-log', action='store_true', default=False, help="Disable clearing of log file on runtime")

parser.add_argument('--progress', action='store_true', default=False, help="Enable progress bar while checking.")

# selenium
parser.add_argument('--webdriver', choices=['chrome', 'firefox'], help="Specify webdriver used for selenium plugins")
parser.add_argument('--selenium-headless', action='store_true', default=False, help="Enable headless excecution of selenium plugins. compatible only with 'chrome' webdriver")
parser.add_argument('--no-selenium', action='store_true', default=False, help="Disable plugins requiring selenium") # disable selenium plugins

# plugins
parser.add_argument('--disable-plugins', default=None, help="Disable plugin(s) on gather. Accepts comma-delimited basenames")


args = parser.parse_args()


# set defaults if necessary; they change depending on action
if args.action == 'check':

    args.input = args.input if args.input else pathlib.Path('output/scraped.json')
    args.output = args.output if args.output else pathlib.Path('output/live.json')

if args.action == 'gather':

    args.output = args.output if args.output else pathlib.Path('output/scraped.json')


# check validity of args
# TODO make this not run each damn time
# DISABLED DUE TO CIRCULAR IMPORT
# if args.action == 'check' and args.input:
#     if not args.input.exists():
#         message = f"[ERROR] Input file located at '{args.input}' not found"
#         log.error(message)
#         raise FileNotFoundError(message)

# if args.threads < 1:
#     message = f"[ERROR] Specified thread count '{args.threads}' not valid"
#     log.error(message)
#     raise ValueError(message)

# if args.timeout < 1:
#     message = f"Specified timeout of '{args.timeout}' seconds not valid."
#     log.error(message)
#     raise ValueError(message)
