"""
config.py -Configuration Helper
Author: Ian Whyman <ian.whyman@sabayon.org>
About: v00d00.net
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def get_config_dir():
	'''returns the current configuration directory'''
	path = os.getenv('PHENNY_CONFIG_DIR')
	if path is None:
		logger.info("PHENNY_CONFIG_DIR var was empty, using default")
		path = os.path.join(os.path.dirname(__file__), 'config')
	return os.path.abspath(path)

def get_config_file_path(name):
	'''returns a path to a file if it exists, otherwise None'''
	path = os.path.join(get_config_dir(), name + '.json')
	if os.path.isfile(path):
		return path
	else:
		logger.warn("Path '%s' is not a file" % path)
		return None

def read_config_file(name):
	'''parses a json configuration file and returns it'''
	path = get_config_file_path(name)
	if path:
		try:
			file = open(path)
			try:
				return json.load(file)
			except ValueError:
				logger.warn("Failed to parse '%s'" % path)
		except IOError:
			logger.warn("Caught exception when opening '%s'" % path)
	else: return None

