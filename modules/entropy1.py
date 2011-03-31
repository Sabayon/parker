#!/usr/bin/env python
"""
ping.py - Phenny Entropy Module.
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""

import urllib2
import json

def entropy(phenny, input):
	if len(input.group(1)) < 3:
		phenny.reply('Sorry, you need to provide at least 3 characters')
		return

	try:
		url ='http://packages.sabayon.org/search?q=' + urllib2.quote(input.group(1)) + '&r=sabayonlinux.org&a=amd64&p=standard&b=5&api=0&render=json'
	except KeyError:
		phenny.reply('Sorry, Could not build request, \'%s\' must not be decodeable to URL safe characters' % input.group(1))
		return

	try:
		f = urllib2.urlopen(url)
		data = f.read()
	except urllib2.HTTPError, e:
		phenny.say('API not found')
		print 'Error code: ', e.code
		return
	except urllib2.URLError, e:
		phenny.say('API not found')
		print 'Reason: ', e.reason
		return

	a = json.loads(data)
	data = {}
	
	if not a.get('5'):
		phenny.reply('Sorry, \'%s\' was not found, or the API thought your terms were to broad, it doesnt like categories too.' % urllib2.quote(input.group(1)))
		return

	for i in a['5']:
		simpleatom = i['category'] + '/' + i['name']
		rev = ':r' + str(i['revision'])
		version = i['atom'][len(simpleatom) + 1:]

		# If we have a revision add it
		if i['revision']:
			version = version + rev

		# Remove annoying trailign slash from URIs
		if i['homepage'][-1:] == '/':
			i['homepage'] = i['homepage'][:-1]

		if not simpleatom in data:
			data[simpleatom] = {}
			data[simpleatom]['name'] = simpleatom
			data[simpleatom]['desc'] = i['description']
			data[simpleatom]['vers'] = [version]
			data[simpleatom]['uri'] = i['homepage']
			data[simpleatom]['dl'] = i['ugc']['downloads']
		else:
			if not version in data[simpleatom]['vers']:
				data[simpleatom]['vers'].append(version)

		if '#' in version:
			x = version.split('#')
			if not data[simpleatom].get('kvers'):
				data[simpleatom]['kvers'] = {x[0]: [x[1]]}
			else:
				if not data[simpleatom]['kvers'].get(x[1]):
					data[simpleatom]['kvers'][x[0]] = [x[1]]
				else:
					data[simpleatom]['kvers'][x[0]].append(x[1])

	counter = 0
	for i in sorted(data, key=lambda x: data[x]['dl'], reverse=True):
		if counter > 3:
			phenny.say('Listed top 4 matches, %d total' % (len(data)))
			return
		i = data[i]
		k = '[%s] %s ' % (i['name'], i['desc'])
		if not i.get('kvers'):
			phenny.say(k + 'v:%s - %s' % (', '.join(sorted(i['vers'], reverse=True)), i['uri']))
		else:
			out = 'v:'
			for v in i['kvers']:
				out += v + ':[' + ', '.join(sorted(i['kvers'][v], reverse=True)) + '] '
			out += ' - %s\n' % (i['uri'])
			phenny.say(k + out)
		counter += 1
		
entropy.rule = r'^\.etp\s(.*)'
entropy.commands = ['.etp']
entropy.example = '.entropy <search>'

if __name__ == '__main__':
   print __doc__.strip()
