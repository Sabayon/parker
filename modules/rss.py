#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rss.py - RSS Announce Module
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""

import feedparser
import json
import time
import logging
import sys

sys.path.append('..')
import conf

logger = logging.getLogger(__name__)
interval = 60

def rss(phenny):
	feeds = conf.read_config_file('rss-feeds')
	if feeds is None:
		logger.debug('Failed to load feeds list, exiting')
		return

	while True:
		for feed in feeds:
			if feed.get('uri'):
				if feed.get('etag'):
					d = feedparser.parse(feed.get('uri'), etag=feed.get('etag'))
				elif feed.get('modified'):
					d = feedparser.parse(feed.get('uri'), modified=feed.get('modified'))
				else:
					d = feedparser.parse(feed.get('uri'))
				
				if d.status is 304:
					logger.debug('%s produced a 304')
					continue
				if d.status != 200:
					logger.warn('%s produced a %d' % (feed.get('uri'), d.status))
					continue
				else:
					if len(d.entries) > 0:
						out = '[%s] New Post: %s - %s' % (feed.get('name'),
									d.entries[0].get('title'), d.entries[0].get('link'))
						if feed.get('previous') == out:
							logger.debug('Skipping duplicate')
							continue

						for channel in feed.get('announcement-channels'):
							phenny.bot.msg(channel, out);
						feed['previous'] = out
						logger.debug('printed ' + out)
					else:
						logger.warn("feed '%s' has zero elements" % feed.get('name'))

					if d.get('etag'):
						feed['etag'] = d.get('etag')
					elif d.get('modified'):
						feed['modified'] = d.get('modified')
			else:
				logger.warn("feed '%s' does not have a uri element" % feed)
	sleep(60)

def run(phenny, input):
	rss(phenny)

run.rule = r'(.*)'
run.event = '255' # RPL_USERME

if __name__ == '__main__':
	print __doc__.strip()
