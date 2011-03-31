#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
factsdb.py - Phenny Personality Module
Copyright 2010, Ian Whyman, ian.whyman@sabayon.org
Licensed under the GPLv3

http://v00d00.net
"""
from pysqlite2 import dbapi2 as sqlite
from random import choice as rdm
"""
Make the DB
csr.execute('CREATE TABLE names (id INTEGER PRIMARY KEY,keyword VARCHAR(20), irctext VARCHAR(140))')
connection.commit()

TODO:
* > operator to send to people
* PERMISSIONS!!!
"""

# borrowed from the factsdb module
def do_db2(command, keywd, args=None):
	# Define DB
	connection = sqlite.connect('botpersonality.sqlite.db')
	csr = connection.cursor()
	keyword = keywd.lower()
	if command == 'add':
		csr.execute('INSERT INTO names VALUES (null, ?,?)',(keyword, args))
		connection.commit()
		return 'Learnt ' + keyword
	elif command == 'del':
		csr.execute('DELETE FROM names WHERE keyword = ?',(keyword,))
		connection.commit()
		return 'Removed ' + keyword + ' from the DB, Bye Bye!'
	elif command == 'search':
		csr.execute('SELECT * FROM names WHERE keyword = ?',(keyword,))
		return csr.fetchall()

def getargs(comnum, string):
	irctext = string.split()
	args = ' '.join(irctext[comnum:len(irctext)])
	return args

def personalitytalk(phenny, input):
	irctext = input.split()
	results = do_db2('search', getargs(1, input))
	resultslst = []
	for result in results:
		if resultslst.count(result[1]) > 0:
			pass # it already exists so skip
		else:
			resultslst.append(result[2])
	if len(resultslst) == 0: # check we found something
		pass
	else:
		#print a random one
		phenny.reply(rdm((resultslst)))

personalitytalk.rule = r'^ParkerBeta(,|:)'
personalitytalk.priority = 'low'
personalitytalk.example = 'None'

def personalitylearn(phenny, input):
	#print '2 ' + input.group(2)
	#print '3 ' + input.group(3)
	phenny.reply(do_db2('add', input.group(2), input.group(3)))
	#elif irctext[1] == 'unlearn':
		#phenny.reply(do_db2('del', getargs(2, input)))

personalitylearn.rule = r'^ParkerBeta(,|:) learn #(.*)#(.*)#'
personalitylearn.priority = 'low'
personalitylearn.example = 'ParkerBeta learn #<trigger>#<response>#'

def personalityforget(phenny, input):
	#print '2 ' + input.group(2)
	phenny.reply(do_db2('del', input.group(2)))

personalityforget.rule = r'^ParkerBeta(,|:) forget #(.*)#'
personalityforget.priority = 'low'
personalityforget.example = 'ParkerBeta forget #<trigger>#'

if __name__ == '__main__':
   print __doc__.strip()
