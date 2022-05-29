ProxySuite - A proxy scraper and checker
========================================

Usage
-----

`python3 main.py gather`

Gathers all proxies to `output/scraped.txt`

`python3 main.py check`

Checks all proxies from `output/scraped.txt` and writes to `output/live.json`

`-b, --basic`

Use faster basic check function 

`-t, --timeout` (int) (default: 15)

Specify timeout duration of http requests

`-T, --threads` (int) (default: 500)

Specify number of synchronous checking threads

`-i, --input` (path) (optional)

Specify input path for checking

`-o, --output` (path) (optional)

Specify output path for checking or gathering. Checking outputs a json, while gahtering outputs plain text.


Design
------

The checker uses synchronous request with paralell threading (default 500) to check each proxy, whether it has ssl supported, the fraud detection score and the whois data. I decided to use threading as the async http module for python has poor socks proxy support. Fraud score is checked as many services will not work on blacklisted ips.


Modifications
-------------

You can add/remove plain text sources by adding them to the list at `data/sources.py`. This is handled by the file `plugins/txt.py`.

In order to add sources which require complex parsing, you can copy `plugins/template.py` to for example `plugins/myplugin.py`. Then make the required edits to return a list of proxies with protocol as a list. The module will be automatically loaded and run when gathering if done correctly.


Future Plans
------------

- [X] Rework cli arguments
- [X] Rework gather code
- [X] Add more user options
- [X] Abitity to enable basic checks

and more...