#!/usr/bin/python3

import os
import threading
import re
import imp

from arguments import args
from logger import log


def gather_all():
    
    plugins = os.listdir("plugins")

    plugins.remove('__pycache__')
    plugins.remove('template.py')
    plugins.remove('spys_one.py') # currently broken

    if args.disable_plugins:
        for plugin in args.disable_plugins.split(','):
            if plugin[-2:] == 'py':
                if plugin in plugins:
                    plugins.remove(plugin)
                    log.debug(f"Disabled plugin {plugin}")
                else:
                    log.warn(f"Plugin specified for disable '{plugin}' not found. Continuing...")

    if args.no_selenium:
        plugins.remove('cyberhub_pw.py')
        log.debug(f"Disabled selenium-based plugins")

    global grabbed
    grabbed = []
    threads = []
    l = threading.Lock()
    
    for i,plugin_name in enumerate(plugins):
        plugin_path = "plugins" + os.sep + plugin_name
        x = threading.Thread(target=worker, args=(plugin_path, l))
        threads.append(x)
        log.debug(f"Created thread {i} for plugin {plugin_path}")

    for i,x in enumerate(threads):
        x.start()
        log.debug(f"Spawned thread {i}")
        
    for i,x in enumerate(threads):
        x.join()
        log.debug(f"Gather task on thread {i} complete")
    
    return grabbed


def worker(plugin_path, l):
    
    global grabbed
 
    try:
        m = imp.load_source('module', plugin_path)
        g = m.Grabber()
    
    except Exception:
        log.exception(f"Failed to load module at {plugin_path}")
        return

    try:
        thread_grabbed = g.grab_all()
        grabbed += thread_grabbed
        log.debug(f"Successfully gathered from plugin '{plugin_path}'")
    
    except Exception:
        log.exception(f"Failed to gather proxies for source '{plugin_path}'")
        return