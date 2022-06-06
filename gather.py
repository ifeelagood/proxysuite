#!/usr/bin/python3

import os
import glob
import threading
import imp

import proxy
from arguments import args
from logger import log

import gather_plain as txt


# address list type is list of 2 element tuples

def gather_all():

    plugins = load_plugins()

    threads = []
    lock = threading.Lock()

    address_list = []

    for i,plugin_path in enumerate(plugins):

        x = threading.Thread(target=worker, args=(plugin_path, address_list, lock))
        threads.append(x)

        log.debug(f"Created thread {i} for plugin {plugin_path}")

    for i,x in enumerate(threads):
        x.start()

    for i,x in enumerate(threads):
        x.join()

    log.debug("Plugin threads terminated")

    gather_plain_sources(address_list)

    log.debug("Filtering addresses and creating proxy objects")
    filtered_proxy_list = [proxy.Proxy(t[0],t[1]) for t in address_list if proxy.validate_address(t[0])]

    log.info(f"Successfully gathered {len(filtered_proxy_list)} proxies!")

    return filtered_proxy_list


def load_plugins(plugin_dir="plugins"):

    plugins = glob.glob(plugin_dir+os.sep+'*.py')

    plugins.remove('plugins/template.py')
    plugins.remove('plugins/spys_one.py') # currently broken USE SELENIUM INSTEAD OF RETARDED DEOBSF

    if args.disable_plugins:
        for plugin in args.disable_plugins.split(','):
            if plugin in plugins:
                plugins.remove(plugin)
                log.debug(f"Disabled plugin {plugin}")
            else:
                log.warning(f"Plugin specified for disable '{plugin}' not found. Continuing...")

    if args.no_selenium:
        plugins.remove('cyberhub_pw.py') #TODO dynamically do this
        log.debug("Disabled selenium-based plugins")

    return plugins


def gather_plain_sources(address_list):

    txt_gathered = txt.grab_all()
    address_list += txt_gathered
    log.debug("Completed gathering from plain text sources")


def worker(plugin_path, address_list, lock):

    try:
        m = imp.load_source('module', plugin_path)
        g = m.Grabber()

    except Exception:
        log.exception(f"Failed to load module at {plugin_path}")
        return

    try:
        raw_thread_address_list = g.grab_all()
        log.debug(f"Successfully gathered from plugin '{plugin_path}'")

    except Exception:
        log.exception(f"Failed to gather proxies for source '{plugin_path}'. Printing trace: ")
        log.warning(f"Continuing after error, results for plugin '{plugin_path}' not scraped")
        log.warning(f"Consider disabling plugin with arguments '--disable-plugins {plugin_path}'")
        return

    thread_address_list = [(address, g.name) for address in raw_thread_address_list]

    lock.acquire()
    address_list += thread_address_list
    lock.release()
