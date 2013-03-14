'''
Generates a json file that explains where each file's origin is
'''

#!/usr/bin/env python

import argparse
import json


TARGET_SRC_MAP = {}

def handle_file(script_name):

	with open(script_name, 'r') as script_name_handle:
		for cat_line in script_name_handle:
			cat_line = cat_line.replace('cat', '').strip()
			src_files, target = cat_line.split('>')
			TARGET_SRC_MAP[target] = src_files.split()


if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()
		parser.add_argument('script_name', metavar = 'script-name', help = 'The script name in question for generating the json file')
		return parser.parse_args()

	parsed = parse_cmdline_args()

	handle_file(parsed.script_name)

	with open('stats.json', 'a+') as fp:
		json.dump(TARGET_SRC_MAP, fp)

