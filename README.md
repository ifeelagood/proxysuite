ProxySuite - A proxy scraper and checker
========================================

Basic Usage/Installation
-----

Install requirements with `pip3 install -r requirements.txt`

`python3 main.py {check,gather}`

* Gather uses the plugins in the `plugins/` directory to gather and save proxies to a file (by default `output/scraped.txt`).

* Check reads an input file (default `output/scraped.txt`) and checks them on multiple threads, then writing all working proxies to an output file (default `output/live.txt`) once complete.

**PLEASE RUN `python3 main.py --help` FOR A FULL LIST AND EXPLAINATION OF CLI ARGS**



Design
------

* The checker uses synchronous request with paralell threading (default 500) to check each proxy, whether it has ssl supported, the fraud detection score and the whois data. I decided to use threading as the async http module for python has poor socks proxy support. However, I am going to try an asynchronous branch in the near future. Fraud score is checked not for nefarious activity, but as many services will not work on blacklisted ips.



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

**Q:** *Why? Why even release this for free?* 

**A:** I'm bored, and believe in the open source ideology. Besides, it's written in python so its not like I can really hide my code if I want to.

***

**Q:** *How many threads are safe to use? What happens if I put in too large a value?* 

**A:** Each thread will open a file for a socket and potentially more, and there are limits defined by the OS for the maximum number of open files. There is also an OS defined limit on the amount of threads per process. This can be easily changed on linux with the command `ulimit`, but discretion is advised. Not only this, but too many threads can hammer an internet connection. Whether this is a design/requests flaw or a general resource problem, I lose connection sometimes when using too many theads, and it can take a few minutes to come back.

TL;DR, It depends on OS limits and internet connection, but 500 is considered 'safe' by me and you can increase it to whatever without any lasting damage

***

**Q:** *Is this illegal?/I'm going to sue the shit outta you!*

**A:** This is a major grey area. Most sources used are probably also scrapers and seem to not care very much, as most also sell probably illegally obtained proxies (usually from malware which creates a proxy server on unknowing people's devices). Any questions or concerns, please contact me in private.


***

Planned Upgrades
----------

- [X] Rework cli arguments
- [X] Rework gather code
- [X] Add more user options
- [X] Abitity to enable basic checks
- [X] Logging
- [ ] Add more sources
- [ ] Clean up plugins and create better template
- [ ] Objectify proxies from gather, allowing for plugin/source evaluation
- [ ] Move proxy functions outside class
- [ ] Create proxy object dump utility
- [ ] Create asynchronous branch

and more...