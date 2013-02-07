"""
Core files for handling kba dataset
"""

#!/usr/bin/env python

import gnupg
import json
import os
import subprocess
import sys
import thrift

from BeautifulSoup import BeautifulSoup, SoupStrainer
from cStringIO import StringIO
from multiprocessing import Pool
from thrift import Thrift
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# set the encoding so BeautifulSoup doesn't take a dump
# add the files generated by the thrift compiler
sys.path.append('/Users/shriphani/Documents/kba-tools/src/main/python/gen-py')

from kba import ttypes


THREAD_POOL_SIZE = 10  # 10 threads ensures that Bhiksha won't kill the job
KBA_BLOGS_LIST_HANDLE = None
KBA_FORUMS_LIST_HANDLE = None
KBA_OUTLINKS_LIST_HANDLE = None

def handle_kba_stream_file(kba_stream_file):
	"""
	Decrypt, open and grab info
	"""
	global KBA_BLOGS_LIST_HANDLE
	global KBA_FORUMS_LIST_HANDLE

	if kba_stream_file.find('.xz.gpg') < 0:
		return

	after_decrypt = kba_stream_file.replace('.gpg', '')
	after_decompress = after_decrypt.replace('.xz', '')

	os.system('gpg -d ' + kba_stream_file + ' > ' + after_decrypt)
	
	compressed_data = open(after_decrypt).read()
	xz_child = subprocess.Popen(
		['xz', '--decompress'],
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)

	thrifts_data, errors = xz_child.communicate(compressed_data)

	transport = StringIO(thrifts_data)
	transport.seek(0)
	protocol = TBinaryProtocol.TBinaryProtocol(
		TTransport.TBufferedTransport(transport)
	)

	while True:
		stream_item = ttypes.StreamItem()
		try:
			stream_item.read(protocol)

			if kba_stream_file.find('social') >= 0:
				handle_metadata(json.loads(stream_item.source_metadata))
			handle_body(stream_item.body)

			flush_streams()

		except EOFError:
			break

	os.system('rm ' + after_decrypt)

def flush_streams():
	KBA_FORUMS_LIST_HANDLE.flush()
	KBA_BLOGS_LIST_HANDLE.flush()
	KBA_OUTLINKS_LIST_HANDLE.flush()

def handle_metadata(metadata):
	if not metadata.has_key('home_link'):
		return

	if metadata['feed_class'] == 'Forum':
		KBA_FORUMS_LIST_HANDLE.write(metadata['home_link'] + '\n')

	elif metadata['feed_class'] == 'Blog':
		KBA_BLOGS_LIST_HANDLE.write(metadata['home_link'] + '\n')

def handle_body(body):
	for link in BeautifulSoup(body.raw, parseOnlyThese=SoupStrainer('a')):
		if link.has_key('href'):
			KBA_OUTLINKS_LIST_HANDLE.write(link['href'] + '\n')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: python kba_core.py <kba_corpus_directory>'
		sys.exit(1)

	KBA_CORPUS_DIRECTORY = sys.argv[1]

	reload(sys)
	sys.setdefaultencoding('utf-8')

	KBA_BLOGS_LIST_HANDLE = open('kba_blogs.txt', 'w')
	KBA_FORUMS_LIST_HANDLE = open('kba_forums.txt', 'w')
	KBA_OUTLINKS_LIST_HANDLE = open('kba_outlinks.txt', 'w')

	p = Pool(THREAD_POOL_SIZE)

	for root, dirs, files in os.walk(KBA_CORPUS_DIRECTORY):	
		if files != []:
			p.map(
				handle_kba_stream_file, 
				[os.path.join(root, f) for f in files]
			)