#!/usr/bin/python3
import data.sources
from core import Proxy
from plugins import txt, free_proxy_list, spys_me, spys_one, checkerproxy_net, openproxy, proxies_wtf


# TODO instead of manually going through each plugin, find a way to iterate through them
# TODO implement type selection
# TODO update all code to asyncio and aiohttp
# TODO clean up plugins and create basic template

def gather_all():

	sources = dict(http=data.sources.HTTP,socks4=data.sources.SOCKS4, socks5=data.sources.SOCKS5)

	grabbed = []

	proxydb = [line.rstrip('\n') for line in open('data/proxydb.txt', 'r').readlines()]
	grabbed += proxydb

	g = txt.Grabber(sources)
	grabbed += g.grab_all()

	g = free_proxy_list.Grabber()
	grabbed += g.grab_all()

	g = spys_me.Grabber()
	grabbed += g.grab_all()

	g = spys_one.Grabber()
	grabbed += g.grab_all()

	g = checkerproxy_net.Grabber()
	grabbed += g.grab_all()

	g = openproxy.Grabber()
	grabbed += g.grab_all()


	g = proxies_wtf.Grabber()
	grabbed += g.grab_all()

	return grabbed
