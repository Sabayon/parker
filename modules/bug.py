#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ping.py - Phenny Bug Linker
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""
import re
import urllib2
import json
bugzillas = [('Sabayon', 'https://bugs.sabayon.org'), ('Gentoo', 'https://bugs.gentoo.org')]

def get_bug(bug_id):
	for bz in bugzillas:
		bug = fetch_bug(bz, bug_id)
		if bug:
			return bug

def fetch_bug(base, bug_id):
	uri = '%s/jsonrpc.cgi?method=Bug.get&params=[{%%20%%22ids%%22:%%20[%d]}]' % (base[1], bug_id)
	try:
		f = urllib2.urlopen(uri)
		data = json.load(f)
	except urllib2.HTTPError as e:
		print 'Error code: ', e.code
		return None
	except urllib2.URLError as e:
		print 'Reason: ', e.reason
		return None
	if data.get('error'):
		print data['error']['message']
		return None
	try:
		data = data['result']['bugs'][0]
		data['bz_name'] = base[0]
		data['bz_uri'] = base[1]
	except KeyError:
		print 'KeyError: ' + data
		return None
	return data

def format_bug(bug_data):
	status = bug_data.get('status')
	if status == 'RESOLVED':
		status = bug_data.get('resolution', 'Unknown Resolution')
	return '[%s Bug %d] %s: %s (%s) %s/%d' % (
		bug_data.get('bz_name', ''),
		bug_data.get('id', 'Unknown Id'),
		bug_data.get('product', 'Unknown Product'),
		bug_data.get('summary', 'Unknown Summary'),
		status,
		bug_data.get('bz_uri', 'Host Unknown'),
		bug_data.get('id', 'Unknown Id'))

def bug(phenny, input):
	print input.groups(0)
	bugid = int(input.groups(0)[0])
	bug = get_bug(bugid)
	if not bug:
		phenny.say('[Bug %s] Bug not found' % bugid)
		return
	phenny.say(format_bug(bug))

bug.rule = r'[Bb][Uu][Gg][\s?#?]+(\d+)'
bug.commands = ['bug #<bug number>']
bug.example = 'Bug #1234'

if __name__ == '__main__':
	print __doc__.strip()
