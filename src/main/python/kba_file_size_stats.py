'''
Computes file size stats for repackaging KBA.
'''

import argparse
import os
import kba_gzip_handler

	
if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument('files_list', metavar = 'files-list', help = 'List of KBA files to deal with.')
		parser.add_argument('output_directory', metavar = 'output-directory', help = 'Directory to place new KBA files')

		return parser.parse_args()

	parsed = parse_cmdline_args()

	with kba_gzip_handle in open(parse_cmdline_args().files_list):
		for new_line in kba_gzip_handler:
			print os.path.abspath(new_line), os.path.getsize(new_line)