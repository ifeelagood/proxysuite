ProxySuite - A proxy scraper and checker
========================================

Basic Usage/Installation
-----

Install requirements with `pip3 install -r requirements.txt`

`python3 main.py {check,gather}`

* Gather uses the plugins in the `plugins/` directory to gather and save proxies to a file (by default `output/scraped.txt`).

* Check reads an input file (default `output/scraped.json`) and checks them on multiple threads, then writing all working proxies to an output file (default `output/live.json` and `output/raw/(http|socks4|socks5).txt`) once complete.

**PLEASE RUN `python3 main.py --help` FOR A FULL LIST AND EXPLAINATION OF CLI ARGS**



Design
------

* The checker uses asyncronous requests with a defined open connection limit, whether it has ssl supported, the fraud detection score and the whois data (whois and fraud detection score can be turned off with --basic/-b). Fraud score is checked not for nefarious activity, but as many services will not work on blacklisted ips.



Modifications
-------------

* You can add/remove plain text sources by adding them to the list at `data/sources.py`. This is handled by the file `plugins/txt.py`. In order to check if a source returns plain text, simply run `curl --user-agent $UA $URL`, note user agent may not always be needed but helps with evading robots.txt

* In order to add sources which require complex parsing, you can copy `plugins/template.py` to for example `plugins/myplugin.py`. Then make the required edits to return a list of proxies with protocol as a list. The module will be automatically loaded and run when gathering if done correctly.



FAQ / Notes
-----------

***

**Q:** *GUI WHEN?*

**A:** I am working on an IPython notebook which will be pushed to main in the near future. This should make it easier for non-gui users.

***

**Q:** *What is the open connection limit (-L)? Which value for this is safe?*

**A:** As this code is asynchronous, if no limit was set the code would keep opening connections for each proxy until the list is exhausted. This leads to the OS Error "Too many open files", as well as sending way too many packets. Through tests I've determined setting this too high can introduce false positives, so I suggest lowering this and testing if the results change.

TL;DR, It depends on OS limits for open files and internet connection, but 1024 is considered 'safe' by me and you can increase it to whatever without any lasting damage

***


Planned Upgrades
----------

- [X] Rework cli arguments
- [X] Rework gather code
- [X] Add more user options
- [X] Abitity to enable basic checks
- [X] Logging
- [ ] Add more sources
- [_] Clean up plugins and create better template
- [X] Objectify proxies from gather, allowing for plugin/source evaluation
- [X] Move proxy functions outside class
- [X] Create proxy object dump utility
- [X] Create asynchronous branch

and more...