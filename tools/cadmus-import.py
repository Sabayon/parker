#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3 as sqlite
import fileinput

connection = sqlite.connect('botbrains.sqlite.db.2')
csr = connection.cursor()

paths = ['/home/wael/.eggdrop/Cadmus/var/quote.dat', '/home/wael/.eggdrop/Cadmus/var/learn.dat']

for path in paths:
	for line in fileinput.input(path):
		items = line.split(' ')
		user = items[0]
		keyword = items[1].lower()
		message = ' '.join(items[2:]).rstrip()
		#csr.execute('INSERT INTO names VALUES (null, ?,?)',(keyword, args))
		#print 'Added ' + keyword + ' to DB'
		if keyword:
			csr.execute('SELECT * FROM names WHERE keyword=?', (keyword,))
			if not csr.fetchone():		
				print user + ' @@ ' + keyword  + ' >> ' + message
				#csr.execute('INSERT INTO names VALUES (null, ?,?)',(keyword, args))

				
#print entries 


#connection.commit()
