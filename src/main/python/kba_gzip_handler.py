"""
This module will allow you to read in a KBA file
"""

import argparse
import gzip
import os
import json
import sys

from cStringIO import StringIO
from thrift import Thrift
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# set the encoding so BeautifulSoup doesn't take a dump
# add the files generated by the thrift compiler
# sys.path.append('/home/spalakod/kba-tools/src/main/python/gen-py') # workhorse settings
# FIXME!: REMOVE THIS MAGIC STRING
# sys.path.append('/Users/shriphani/Documents/kba-tools/src/main/python/gen-py')
sys.path.append('/bos/usr3/spalakod/kba-tools/src/main/python/gen-py')

from kba import ttypes


def handle_gzip_kba_social_file(gzip_file):
	kba_stream = gzip.open(gzip_file)
	transport = StringIO(kba_stream.read())
	transport.seek(0)
	protocol = TBinaryProtocol.TBinaryProtocol(TTransport.TBufferedTransport(transport))

	while True:
		stream_item = ttypes.StreamItem()
		try:
			stream_item.read(protocol)
			yield stream_item

		except EOFError:
			break

if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument('gzip_files_list', metavar = 'gzip-files-list', help = 'Name of gzipped KBA file')
		parser.add_argument('--output-directory', dest = 'output_directory', help = 'Directory to place the generated file')
		parser.add_argument('--dump-home-urls', action = 'store_true', dest = 'dump_home_urls', default = False)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	with open(parsed.gzip_files_list, 'r') as gzip_files_handle:
		for gzip_filename in gzip_files_handle:
			handle_gzip_kba_social_file(gzip_filename.strip(), parsed.output_directory)