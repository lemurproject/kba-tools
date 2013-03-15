#!/usr/bin/env python

'''
This script verifies if the repackaged kba files are ok or not
'''

import argparse
import json
import kba_gzip_handler

class KBASourcesError(Exception):
	pass


def verify(target_file, sources):

	target_file_kba_generator = kba_gzip_handler.handle_gzip_kba_social_file(target_file)

	for source_file in sources:
		for stream_object in kba_gzip_handler.handle_gzip_kba_social_file(source_file):
			target_stream_object = target_file_kba_generator.next()

			if stream_object != target_stream_object:
				raise KBASourcesError('Fuck up')

	return True


if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument('kba_sources_file', metavar = 'kba-sources-file', help = 'KBA Sources file')

		return parser.parse_args()

	parsed = parse_cmdline_args()

	with open(parsed.kba_sources_file, 'r') as kba_sources_file_handle:
		target_source_map = json.load(kba_sources_file_handle)

		for target, sources_list in target_source_map.iteritems():
			verify(target, sources_list)