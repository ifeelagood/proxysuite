#!/usr/bin/python3
import plugins.__init__

# TODO implement type selection
# TODO update all code to asyncio and aiohttp


def gather_all():

	grabbed = plugins.__init__.__gather_all__()
	return grabbed
