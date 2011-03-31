#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
factsdb.py - Phenny User Rights Module
Copyright 2010, Ian Whyman, ian.whyman@sabayon.org
Licensed under the GPLv3

http://v00d00.net
"""
#/who!
def who(phenny, input):
	irctext = input.split()
	phenny.say('/who ' + irctext[1])

who.rule = r'^\.who\s'
who.commands = ['.who']
who.example = '.who <targeted user>'

if __name__ == '__main__':
   print __doc__.strip()
