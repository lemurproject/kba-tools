'''
Generate repackage scripts
'''

import sys

def produce_condor_script(prefixes):
	for prefix in prefixes:
		print 'condor_run \"python /bos/usr3/spalakod/kba-tools/src/main/python/kba_repackager.py /bos/tmp19/spalakod/kba-stream-corpus-2012/ %(prefix)s /bos/usr3/spalakod/kba_repack/\"' % { 'prefix':prefix }


if __name__ == '__main__':
	prefix_list = sys.argv[1]

	f = open(prefix_list, 'r')
	prefixes = map(lambda s: s.strip(), f.readlines())

	produce_condor_script(prefixes)