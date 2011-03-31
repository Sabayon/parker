#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
factsdb.py - Phenny Quotes Module (2.0)
Copyright 2010, Ian Whyman, ian.whyman@sabayon.org
Licensed under the GPLv3

http://v00d00.net
"""
import sqlite3 as sqlite
from random import choice as rdm
import datetime

def do_db(command, keywd, args=None, nickname=None, rmid=None):
	# Define DB
	connection = sqlite.connect('botbrains.sqlite.db')
	csr = connection.cursor()
	keyword = str.lower((str(keywd)))
	if command == 'add':
		csr.execute('INSERT INTO names VALUES (null, ?,?,?,?)',(keyword, args, datetime.datetime.now(), nickname))
		connection.commit()
		return 'Added ' + keyword + ' to DB successfully. Author: ' + str(nickname) + ' Time: ' + datetime.datetime.now().isoformat()
	elif command == 'get':
		csr.execute('SELECT * FROM names WHERE keyword = ? ORDER BY id ASC',(keyword,))
		return csr.fetchall()
	elif command == 'del':
		if rmid != None:
			csr.execute('SELECT id FROM names WHERE keyword = ? ORDER BY id LIMIT ?, 1',(keyword,rmid,))
			if csr.fetchone() != None:
				csr.execute('DELETE FROM names WHERE id IN ( SELECT id FROM names WHERE keyword=? ORDER BY id LIMIT ?, 1 )',(keyword,rmid,))
				connection.commit()
				return 'Removed item #%s for %s from the DB' % (rmid,keywd)
			else:
				return 'Item  #%s for \'%s\' not found.' % (rmid,keywd)
		else:
			csr.execute('DELETE FROM names WHERE keyword = ?',(keyword,))
			connection.commit()
			return 'Removed all items for ' + keyword + ' from the DB'
	elif command == 'search':
		csr.execute('SELECT * FROM names WHERE (keyword like ?) or (data like ?) ORDER BY id ASC',('%' + keyword + '%', '%' + keyword + '%',))
		return csr.fetchall()

def getargs(comnum, string):
	irctext = string.split()
	args = ' '.join(irctext[comnum:len(irctext)])
	return args
	
def add_botdb(phenny, input):
	irctext = input.split()
	# .donky-0 add-1 spam-2 woohoo-3 string-4
	phenny.say(do_db(command='add', keywd=irctext[2], args=getargs(3, input), nickname=input.nick))

add_botdb.rule = r'^\? add [\w\d-]'
add_botdb.priority = 'low'
add_botdb.example = '? add <keyword> <text>'

def del_botdb(phenny, input):
	irctext = input.split()
	if len(irctext) == 4:
		phenny.say(do_db(command='del', keywd=input.group(1), rmid=input.group(3)))
	else:
		phenny.say(do_db(command='del', keywd=input.group(1)))
	
del_botdb.rule = r'^\? rm ([\w\d-]+)(\s)?(\d)?$'
del_botdb.priority = 'low'
del_botdb.example = '? rm <keyword> [entry number to remove]'

def search_botdb(phenny, input):
	results = do_db(command='search', keywd=input.group(2))
	resultslst = []
	for result in results:
		if resultslst.count(result[1]) > 0:
			pass # it already exists so skip
		else:
			resultslst.append(result[1])
	if len(resultslst) == 0: # check we found something
		phenny.reply('No results found for \"%s\"%s' % (input.group(2), rdm(('', ', sorry!', ', blame AjeZ!',))))
	else:
		phenny.reply('Search results for \"%s\": %s' % (input.group(2), ', '.join(resultslst)))
		
search_botdb.rule = r'^\? (f|find|search) (\w*)'
search_botdb.priority = 'low'
search_botdb.example = '? f/find/search <keyword>'

def get_botdb(phenny, input):
	results = do_db(command='get', keywd=input.group(1))
	print input.group(1)
	itemid = 0
	if len(results) > 0:
		for result in results:
			phenny.say('[%d] %s: %s' % (itemid, input.group(1), result[2]))
			itemid = itemid + 1
	else:
		phenny.say(input.group(1) + ': Not Found' +
		rdm(('!', ', I hope I havent lost it?',
		', you didnt really want to see that anyway!',
		', no joy old chap.', ', blame AjeZ!',)) + ' Maybe search using: \"? find <term>\"?')

get_botdb.rule = r'^\? ([\w\d-]*)$'
get_botdb.priority = 'low'
get_botdb.example = '? <keyword>'


def cadmus_compat(phenny, input):
	if input.group(1) == 'add':
		phenny.say(do_db(command='add', keywd=input.group(2), args=getargs(3, input), nickname=input.nick))
	elif input.group(1) == 'del':
		phenny.say(do_db(command='del', keywd=input.group(2)))
	else:
		pass

cadmus_compat.rule = r'\!learn (add|del) ([\w\d-]+)'
cadmus_compat.priority = 'low'
cadmus_compat.example = ''

if __name__ == '__main__':
   print __doc__.strip()
