'''
Cat an save it.
'''

import os
import sys


OUTPUT_DIRECTORY = '/bos/tmp19/spalakod/kba-stream-corpus-repack-2012'

if __name__ == '__main__':

	prefix_dirs = sys.argv[1]

	for root, dirs, files in os.walk(prefix_dirs):
		for dirname in dirs:
			result_dirname = os.path.join(OUTPUT_DIRECTORY, dirname)
			os.mkdir(result_dirname)

		for filename in files:
			result_dirname = os.path.join(OUTPUT_DIRECTORY, os.path.basename(root))
			fname = os.path.splitext(filename)[0] + '.gz'

			f = open(os.path.join(root, filename), 'r')

			script = 'condor_run \"cat '

			for new_line in f:
				script += new_line.strip() + ' '

			script += '> ' + os.path.join(result_dirname, fname) + ' &\" &'
			print script

			f.close()

