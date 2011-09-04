#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
welcomeer.py - Phenny Greeting module
Copyright 2011 - Ian Whyman <ian.whyman@sabayon.org>
Licensed under the GPLv3

http://v00d00.net
"""
import random
import re

greetings = [
	'Ahoy there',
	'G\'day',
	'Greetings',
	'Hello',
	'Hello there',
	'Hey',
	'Hi',
	'Hi there',
	'Welcome',
	'Yo',
	'Sup',
	'Bienvenue',
	'Willkommen',
	'Aloha',
	'Welkom',
	'Bienvenido',
]
thanks = [
	'much obliged',
	'thanks',
	'thank you',
	'cheers',
]
names = re.compile(r'sabayon(web|user)(.+)?')

def send_info(phenny, nick, channel):
		msg = "%s %s. Welcome to %s! I hope you enjoy your stay. \
I see you have a generic nick, please change it to something that identifies you \
individually as it will aid other users in communicating with you. \
You can do this by typing this command into your chat box: \
\"/nick YourNewNickHere\", %s!" % (random.choice(greetings), nick, channel, random.choice(thanks))
		phenny.bot.msg(nick, msg)
		phenny.bot.msg(nick, "Please feel free to ask your question \
straight away, do not ask to ask! Do not paste in the channel, use a pastebin such \
as http://pastebin.sabayon.org then provide the link that is generated.")

def welcomer(phenny, input):
	if names.match(input.nick):
		send_info(phenny, input.nick, input.group(0))

welcomer.rule = r'(.*)'
welcomer.event = 'JOIN'
welcomer.example = '.test'

if __name__ == '__main__':
   print __doc__.strip()
