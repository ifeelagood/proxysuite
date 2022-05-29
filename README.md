ProxySuite - A proxy scraper and checker
========================================

Usage
-----

`python3 main.py gather`

Gathers all proxies to `output/scraped.txt`

`python3 main.py check`

Checks all proxies from `output/scraped.txt` and writes to `output/live.json`


Better cli args planned for future.

Design
------

The checker uses threads (default 500) to check each proxy, whether it has ssl supported, the fraud detection score and the whois data. I decided to use  threading as the async http module for python has poor socks proxy support. Fraud score is checked as many services will not work on blacklisted ips.

Modifications
-------------

You can add more text sources by adding them to the list `data/sources.py

In order to add sources which require complex parsing, you can copy `plugins/template.py` to for example `plugins/myplugin.py`. Then make the required edits to return a list of proxies with protocol as a list. The module will be automatically loaded scraped from is setup correctly

Future Plans
------------

- [ ] Rework cli arguments
- [X] Rework gather code
- [ ] Add more user options
- [-] Abitity to enable basic checks