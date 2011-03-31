#!/usr/bin/env python
"""
roulette.py - Phenny Roulette Module
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""
import random

#def spin(phenny, input):
	#"""Take your chances at roulette."""
	#action = random.choice(('BOOM! Your dead!', 'click, lucky', 'click', 'click', 'Click, you survived ... this time', 'click'))
	#if action == 'BOOM! Your dead!':
		#phenny.reply(action)
		#phenny.say('!kick ' + input.nick)
	#else:
		#phenny.reply(action)

#spin.rule = r'^\.spin$'
#spin.commands = ['.spin']
#spin.example = '.spin'

bulletLocation = 3
chambersLeft = 5
fired = 0

def spin2(phenny, input):
	"""Spin barrell"""
	global fired
	if fired == 0:
		phenny.reply('You\'re spinning again? Pussy.')
	global bulletLocation
	bulletLocation = random.randrange(5)
	#phenny.say('spin2.0')
	#phenny.say('bullet is at location ' + str(bulletLocation))
	phenny.reply('the barrell has been spun! now .pull!')

	global chambersLeft
	chambersLeft= 5
	fired = 0

spin2.rule = r'^\.spin$'
spin2.commands = ['.spin']
spin2.example = '.spin'

def pull(phenny, input):
	global chambersLeft
	global bulletLocation
	global fired

	# reduce the bullet count
	chambersLeft = chambersLeft -1

	if fired == 1:
		phenny.reply('Gun has already been fired, You need to .spin to play again!')
	else:
		if chambersLeft == bulletLocation:
			phenny.reply('Boom! Your Dead! Unlucky sucker')
			phenny.say('!kick ' + input.nick)
			fired = 1
		else:
			phenny.reply(random.choice(('click, lucky', 'click, you live for another round', 'click, phew', 'click!', 'Click, you survived ... this time', 'click')) + ' [' + str(chambersLeft +1) + ' chambers left]')

pull.rule = r'^\.pull$'
pull.commands = ['.pull']
pull.example = '.pull'

if __name__ == '__main__':
   print __doc__.strip()
