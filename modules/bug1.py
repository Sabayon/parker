#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ping.py - Phenny Bug Linker
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""

import re
import urllib2
from xml.sax.saxutils import unescape

def xscape(string):
	# Unescape stuff.
	return unescape(string, {"&apos;": "&", "&quot;": '"'})

def bug1(phenny, input):
	"""Print bug desc"""
	#YAY for Regex 
	bugid = re.search(r'(B|b)ug #?(?P<bugnum>\d*)', input)
	
	#remove leading zeros
	a = int(bugid.group('bugnum'))
	bug_id = str(a)
	
	url ='http://bugs.sabayon.org/show_bug.cgi?id=' + bug_id
	
	try:
		f = urllib2.urlopen(url)
		data = f.read()
	except urllib2.HTTPError, e:
		phenny.say('[Bug %s] Bug not found' % (bug_id))
		print 'Error code: ', e.code
		return
	except urllib2.URLError, e:
		phenny.say('[Bug %s] Bug not found' % (bug_id))
		print 'Reason: ', e.reason
		return
		
	#check its not an error:
	checktitle = re.search(r'(?<=<title>).*(?=</title>)', data).group(0)
	# Not found
	if checktitle == 'Invalid Bug ID | Sabayon Bugzilla':
		phenny.say('[Bug %s] Bug number invalid'  % (bug_id))
		return
	#someone is looking for bug 0
	elif checktitle == 'Search by bug number | Sabayon Bugzilla':
		phenny.say('[Bug %s] Bug not found' % (bug_id))
		return
	else:
		title = re.search(r'(?<=<title>Bug %s &ndash; ).*(?=\ \|\ Sabayon Bugzilla</title>)' % bug_id, data)
		status = re.search(r'(?<=<span id="static_bug_status">).*', data)
		product = re.search(r'(?<=id="field_container_product" >).*(?=</td>)', data)
		
		phenny.say('[Bug %s] %s - %s (%s) %s' % (bug_id, product.group(0),  xscape(title.group(0)), status.group(0), url))
		return
	
bug1.rule = r'(B|b)(U|u)(G|g) #?([0-9])'
bug1.commands = ['bug #<bug number>']
bug1.example = 'Bug #1234'

if __name__ == '__main__':
   print __doc__.strip()
