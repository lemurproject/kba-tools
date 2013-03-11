'''
Runs through a KBA gz file
'''

import argparse
import kba_gzip_handler


if __name__ == '__main__':
	def parse_cmd_line_args():
		parser = argparse.ArgumentParser()
		parser.add_argument('gzip_file', metavar = 'gzip-file', help = 'kba gzip file')
		return parser.parse_args()

	for stream_item in kba_gzip_handler.handle_gzip_kba_social_file(parse_cmd_line_args().gzip_file):
		print stream_item