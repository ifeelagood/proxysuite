#!/usr/bin/python3

import os
import json
import pathlib
import argparse

import checker
import gather

global args

def checker_runner():
    
    checked = checker.check_all(args)

    with open(args.output, 'w') as f:
        json.dump(checked, f)

def gather_runner():
    
    gathered = gather.gather_all()

    if not args.output.parent.exists():
        os.mkdir(args.output.parent)

    with open(args.output, 'w') as f:
        for p in gathered:
            f.write(p + '\n')


def default_io_args():
    
    if args.action == 'check':
        
        args.input = args.input if args.input else pathlib.Path('output/scraped.txt')
        args.output = args.output if args.output else pathlib.Path('output/live.json')
    
    if args.action == 'gather':

        args.output = args.output if args.output else pathlib.Path('output/scraped.txt')
        

def check_args():
    
    if args.action == 'check' and args.input:
        if args.input.exists():
            raise FileNotFoundError(f"[ERROR] Input file located at '{args.input}' not found")
    
    if args.threads < 1:
        raise ValueError(f"[ERROR] Specified thread count '{args.threads}' less than one")
    
    if args.timeout < 1:
        raise ValueError(f"[ERROR] Specified timeout of '{args.timeout}' seconds not valid. Must be greater than or equal to 1.")
    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Scrape and check proxies.')
    parser.add_argument('action', choices=['check', 'gather'])
    parser.add_argument('-b', '--basic', action='store_true', default=False) # couldnt get py3.9 argparse.BooleanOptionalAction to work TODO
    parser.add_argument('-T', '--threads', type=int, default=500)
    parser.add_argument('-t', '--timeout', type=int, default=15)
    parser.add_argument('-o', '--output', nargs=1, type=pathlib.Path, default=None)
    parser.add_argument('-i', '--input', nargs=1, type=pathlib.Path, default=None)
    
    args = parser.parse_args()
    
    check_args()
    default_io_args()
    
    if args.action == 'check':
        checker_runner()
        
    if args.action == 'gather':
        gather_runner()
