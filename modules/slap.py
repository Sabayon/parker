#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ping.py - Phenny Slap Module
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""

import random, re

def slap(phenny, input):
	"""Slap another user in channel."""
	slaction = random.choice((
	'slaps',
	'bashes',
	'ravages'))

	slobject = random.choice((
	'a plate of spam spam spam eggs and spam',
	'the RTFM stick',
	'a sock full of STFU',
	'a wet fish',
	'a ubuntu user',
	'windows 3.1',
	'some Ekki-Ekki-Ekki-Ekki-PTANG. Zoom-Boing. Znourrwringmm',
	'the rear half of a donkey',
	'a holy hand grenade',
	'some live jumper cables',
	'an anvil'))

	if len(input.split()) <= 1:
		phenny.me(slaction + ' ' + input.nick + ' with ' + slobject)

	msgargs = input.split()
	msgargs.remove('.slap')
	sep = ' '
	victim = sep.join(msgargs)

	reg = re.compile("%s*" % phenny.nick)
	if re.match(reg, victim):
		phenny.me(slaction + ' ' + input.nick + ' with ' + slobject)
	else:
		phenny.me(slaction + ' ' + victim + ' with ' + slobject)

slap.rule = r'^\.slap\s'
slap.commands = ['.slap']
slap.example = '.slap <targeted user>'

if __name__ == '__main__':
   print __doc__.strip()
