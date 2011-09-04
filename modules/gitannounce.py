#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gitannounce.py - Phenny Git announcer
Copyright 2011, Ian Whyman, v00d00.net
Licensed under the GPLv2

http://v00d00.net
"""
import json
import os.path
import sys
import SocketServer

with open(os.path.join(os.path.dirname(__file__), 'gitannounce.config.json')) as f:
	config = json.load(f)

def generate_url(repo, commitref):
	return 'https://git.sabayon.org/%s/commit/?id=%s' % (repo, commitref)

def alias_names(user):
	replacements = config['user_replace']
	if user in replacements:
		return replacements[user]
	else:
		return user

class Handler(SocketServer.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		try:
			commit = json.loads(self.data)
		except ValueError:
			print "[Announcer] Json Decode Failed"
			return

		key = commit.get('shared_key')
		if not key == config.get('key'):
			print('[Announcer] Key Mistmatch: Us: %s, Them: %s' % 
				(repr(config.get('key')), repr(key)))
			return

		url = generate_url(commit.get('repository'),
				commit.get('commit'))
		author = alias_names(commit.get('author'))
		if len(commit.get('message')) > 80:
			message = commit.get('message')[:80] + '...'
		else:
			message = commit.get('message')
		output = '[%s] %s: %s %s' % (commit.get('repository'),
						author, message, url)

		if commit.get('repository') in config['channels']:
			channels = config['channels'].get(commit.get('repository'))
		else:
			channels = config['channels'].get('default')
		for channel in channels:
			self.server.phenny.bot.msg(channel, output)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	def __init__(self, server_address, RequestHandlerClass, phenny):
		self.phenny = phenny
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def announce(phenny, input):
	HOST, PORT = "0.0.0.0", 37373
	server = Server((HOST, PORT), Handler, phenny)
	print('Announcer started')
        server.serve_forever()

announce.rule = r'(.*)'
announce.event = '255' # RPL_USERME
announce.priority = 'low'

if __name__ == '__main__':
   print __doc__.strip()
