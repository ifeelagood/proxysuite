#!/usr/bin/python3

import json
import pathlib
import argparse

import checker
import gather

def checker_runner(infile, outfile):
    
    with open(infile, 'r') as f:
        unchecked = [line.rstrip('\n') for line in f.readlines()]

    checked = checker.check_all(unchecked)

    with open(outfile, 'w') as f:
        json.dump(checked, outfile)

def gather_runner(outfile):
    
    gathered = gather.gather_all()

    if not outfile.parent.exists():
        os.mkdir(outfile.parent)

    with open(outfile, 'w') as f:
        for p in gathered:
            f.write(p + '\n')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Scrape and check proxies.')
    parser.add_argument('action', choices=['check', 'gather'])
    # parser.add_argument('-o', '--output', nargs=1, type=pathlib.Path, default=None)
    # parser.add_argument('-i', '--input', nargs=1, type=pathlib.Path, default=None)
    args = parser.parse_args()
    
    # the reason im not setting a default is because it will change between check and gather

    if args.action == 'check':
        
        # infile = args.input if args.input else pathlib.Path('output/scraped.txt')
        # outfile = args.output if args.output else pathlib.Path('output/live.json')
        infile = pathlib.Path('output/scraped.txt')
        outfile = pathlib.Path('output/live.json')
        checker_runner(infile, outfile)


    if args.action == 'gather':

        # outfile = args.output if args.output else pathlib.Path('output/scraped.txt')
        outfile = pathlib.Path('output/scraped.txt')
        gather_runner(outfile)
