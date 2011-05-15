#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rss.py - Phenny Fourth Generation RSS Announce Module
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""
__metaclass__ = type

import feedparser
import urllib2 
import time

feedlist = {
	'overlay' : {
	'url' : 'http://gitweb.sabayon.org/?p=overlay.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},
				
	'artwork' : {
	'url' : 'http://gitweb.sabayon.org/?p=artwork.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},
	
	'entropy' : {
	'url' : 'http://gitweb.sabayon.org/?p=entropy.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},
	
	'planet' : 	{
	'url' : 'http://planet.sabayon.org/?feed=rss',
	'channels' : ['#sabayon-dev', '#sabayon', '#sabayon-social'],
	},

	'entropy-packagekit' : {
	'url' : 'http://gitweb.sabayon.org/?p=packagekit-entropy.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'anaconda' : {
	'url' : 'http://gitweb.sabayon.org/?p=anaconda.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'molecule' : {
	'url' : 'http://gitweb.sabayon.org/?p=molecule.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'skel' : {
	'url' : 'http://gitweb.sabayon.org/?p=skel.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'v00d00-overlay' : {
	'url' : 'http://gitweb.sabayon.org/?p=playground/v00d00.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},
	
	'bugzilla' : {
	'url' : 'http://gitweb.sabayon.org/?p=www/bugzilla.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'molecules' : {
	'url' : 'http://gitweb.sabayon.org/?p=molecules.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'drupal' : {
	'url' : 'http://gitweb.sabayon.org/?p=www/drupal.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'gitweb' : {
	'url' : 'http://gitweb.sabayon.org/?p=www/gitweb.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'static' : {
	'url' : 'http://gitweb.sabayon.org/?p=www/static.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},

	'parker' : {
	'url' : 'http://gitweb.sabayon.org/?p=parker.git;a=rss',
	'channels' : ['#sabayon-dev'],
	},
}
		
name_replacements = {
	'Fabio Erculiani <lxnay@sabayon.org>': 'Lxn4y',
	'Mitch Harder <mitch.harder@sabayonlinux.org>': 'DontPanic',
	'Ian Whyman <ian.whyman@sabayon.org>': 'Thev00d00',
	'Joost Ruis <joost.ruis@sabayonlinux.org>': 'Joost',
	u'Sławomir Nizio <slawomir.nizio@sabayon.org>': 'Enlik'
	}

def name_switch(name_in):
	if name_replacements.get(name_in) != None:
		return name_replacements.get(name_in)
	else:
		return name_in

def get_feed_date(feedname):
	d = feedlist[feedname]
	try:
		request = urllib2.Request(d['url'])
		# if we are just starting
		if d['last_feed_update'] != None:
			request.add_header('If-Modified-Since', time.strftime('%a, %d %b %Y %H:%M:%S %Z', d['last_feed_update']))	
		opener = urllib2.build_opener()
		rssfile = opener.open(request)
	except urllib2.HTTPError, e:
		try:
			e.code
		except NameError:
			print '%s - HTTPError (Reason: No E.Code)' % (d['url'])
			return d['last_feed_update']
		except BadStatusLine:
			print '%s - HTTPError (Reason: BadStatusLine)' % (d['url'])
			return d['last_feed_update']
		else:
			if e.code == 304:
				return d['last_feed_update']
			else:
				print '%s - HTTPError (Code: %s)' % (d['url'], e.code)
				return d['last_feed_update']
	except urllib2.URLError, e:
		try:
			e.code
		except (NameError, AttributeError):
			print '%s - URL-Name/Attribute Error (Reason: No Code Returned)' % (d['url'])
			return
		else:
			print '%s - UrlError (Code: %s)' % (d['url'], e.code)
			return d['last_feed_update']
	else:
		if rssfile.headers.get('Last-Modified') == None:
			print '%s - Last Modified Missing' % (d['url'])
			print rssfile.headers
			return d['last_feed_update']
		else:
			lastmod = time.strptime(rssfile.headers.get('Last-Modified'), '%a, %d %b %Y %H:%M:%S %Z')
			debug_print(lastmod)
			return(lastmod)
		
		
def parse_rss(feedname, entry=0): #entry is rss item number
	d = feedlist[feedname]
	try:
		rss = feedparser.parse(d['url'])
	except urllib2.HTTPError, e:
		try:
			e.code
		except NameError:
			print '%s - HTTPError (Reason: No E.Code)' % (d['url'])
			return
		else:
			print '%s - HTTPError (Reason: %s)' % (d['url'], e.code)
			return
	except urllib2.URLError, e:
		try:
			e.code
		except NameError:
			print '%s - HTTPError (Reason: No E.Code)' % (d['url'])
			return
		else:
			print '%s - UrlError (Reason: %s)' % (d['url'], e.code)
			return
	
	try:
		title = rss.entries[entry].get('title')
		author = name_switch(rss.entries[entry].get('author'))
		link = link = rss.entries[entry].get('link')
		return [author, title, link]
	except IndexError:
		print '%s - Error - IndexError entry(%s) invaild' % (d['url'], entry)
		return

def mainloop(phenny, input):
	while 1 == 1:
		for feed in feedlist:
			time.sleep(15)
			debug_print('Sleeping in ', feed)
			d = feedlist[feed]
			feeddate = get_feed_date(feed)
			if feeddate > d['last_feed_update']:
				# Make sure the feed we have is valid
				if not parse_rss(feed):
					continue

				prss = parse_rss(feed)
				
				if prss is None:
					continue

				# Prevent double posts of the same thing (Fix for Gitweb)
				if prss[1] == d['previous'].get('title'):
					continue
				
				# If its the first run, dont announce, just store
				elif d['previous'].get('title') == None:
					print 'Not announcing ' + feed
					# Update last posted msg
					d['last_feed_update'] = feeddate
					d['previous']['author'] = prss[0]
					d['previous']['title'] = prss[1]
					d['previous']['link'] = prss[2]
					debug_print(d['previous']['author'])
					debug_print(d['previous']['title'])
					debug_print(d['previous']['link'])
					debug_print(d['last_feed_update'])
					continue

				else:
					# Announce the message
					msg = '[%s] %s - %s - %s' % (feed, prss[0], prss[1], prss[2])
					
					debug_print(msg)

					for channel in d.get('channels'):
						# Use phenny.bot.msg() directly
						phenny.bot.msg(channel, msg)

					# Update last posted msg
					d['last_feed_update'] = feeddate
					d['previous']['author'] = prss[0]
					d['previous']['title'] = prss[1]
					d['previous']['link'] = prss[2]
			else:
				continue

def init():
	for feed in feedlist:
		q = feedlist[feed]
		q['last_feed_update'] = None
		q['previous'] = {'author': None, 'title': None, 'link': None}
	global mainloop_running
	mainloop_running = 0
	global debug
	debug = 0


def main(phenny, input):
	global mainloop_running
	if mainloop_running == 0:
		mainloop_running = 1
		mainloop(phenny, input)
	else:
		return
		
main.rule = r'(.*)'
main.priority = 'low'
#main.thread = False

def latest(phenny, input):
	feedname = input.groups()[0]
	prss = parse_rss(feedname)
	phenny.reply('Latest %s: %s - %s - %s' % (feedname, prss[0], prss[1], prss[2]))
	return

latest.rule = r'^\.latest (' + '|'.join(feedlist) + ')'
latest.commands = ['.latest']
latest.example = '.latest <feedname>'
latest.priority = 'high'

def rss4debug(phenny, input):
	global debug
	if debug == 0:
		debug = 1
		phenny.reply('Debugging On')
	else:
		debug = 0
		phenny.reply('Debugging Off')

rss4debug.rule = r'\.rss4debug'
rss4debug.priority = 'low'

def debug_print(*msg):
	global debug
	if debug == 1:
		print msg

# Run Setup
init()

if __name__ == '__main__':
	print __doc__.strip()
