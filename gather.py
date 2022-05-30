#!/usr/bin/python3

import os
import threading
import re
import imp

from proxy import Proxy
from arguments import args
from logger import log

from plugins import txt


def gather_all():
    
    plugins = os.listdir("plugins")

    plugins.remove('__pycache__')
    plugins.remove('template.py')
    plugins.remove('txt.py') # we will deal with you later!
    plugins.remove('spys_one.py') # currently broken USE SELENIUM INSTEAD OF RETARDED DEOBSF

    if args.disable_plugins:
        for plugin in args.disable_plugins.split(','):
            if plugin[-2:] == 'py':
                if plugin in plugins:
                    plugins.remove(plugin)
                    log.debug(f"Disabled plugin {plugin}")
                else:
                    log.warn(f"Plugin specified for disable '{plugin}' not found. Continuing...")

    if args.no_selenium:
        plugins.remove('cyberhub_pw.py') #TODO dynamically do this
        log.debug(f"Disabled selenium-based plugins")

    global grabbed
    grabbed = []
    threads = []
    lock = threading.Lock()
    
    for i,plugin_name in enumerate(plugins):
        plugin_path = "plugins" + os.sep + plugin_name
        x = threading.Thread(target=worker, args=(plugin_path, lock))
        threads.append(x)
        log.debug(f"Created thread {i} for plugin {plugin_path}")

    for i,x in enumerate(threads):
        x.start()
        
    for i,x in enumerate(threads):
        x.join()
    
    log.debug("All threads released for plugins")    

    gather_plain_sources()
    
    log.info("Gathering complete!")
    
    return grabbed


def gather_plain_sources():
    
    global grabbed
    
    g = txt.TXTGrabber()
    txt_gathered = g.grab_all()
    
    unfiltered_proxy_objects = [Proxy(p,s) for p,s in txt_gathered]
    
    included_addresses = []
    proxy_objects = []
    
    for p in unfiltered_proxy_objects:
        if p.address not in included_addresses:
            included_addresses.append(p.address)
            proxy_objects.append(p)

    grabbed += proxy_objects
    log.debug("Completed gathering from plain text sources")


def add_to_grabbed(lst, sourcename, lock):
    
    # yes, there will be duplicates which cross over sources, however when evaluating sources this is useful
    
    global grabbed

    deduped = list(dict.fromkeys(lst)) # dedupe
    
    valid_regex = r'(http|https|socks4|socks5):\/\/(\d{1,3}\.){3}\d{1,3}:(\d+)'
    
    for p in deduped:
        if re.match(valid_regex, p) is None:
            log.debug(f"Removing invalid proxy '{p}' for source '{sourcename}")
            deduped.remove(p)
    

    proxy_objects = [Proxy(p, source=sourcename) for p in deduped]
    
    lock.acquire()
    grabbed += proxy_objects
    lock.release()


def worker(plugin_path, lock):
    
    global grabbed
 
    try:
        m = imp.load_source('module', plugin_path)
        g = m.Grabber()
    
    except Exception:
        log.exception(f"Failed to load module at {plugin_path}")
        return

    try:
        thread_grabbed = g.grab_all()
        log.debug(f"Successfully gathered from plugin '{plugin_path}'")
    
    except Exception:
        log.exception(f"Failed to gather proxies for source '{plugin_path}'")
        return
    
    add_to_grabbed(thread_grabbed, g.name, lock)