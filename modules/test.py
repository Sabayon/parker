#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
startup.py - Phenny Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def test(phenny, input):
	phenny.bot.msg('#test22', 'SPAM!')
	print input.groups()
	print input.args

test.commands = ['.test']
test.example = '.test'

if __name__ == '__main__':
   print __doc__.strip()
