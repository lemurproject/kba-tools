#!/usr/bin/env python

import os
import sys


if __name__ == '__main__':
	a = sys.argv[1]

	with open(a, 'r') as unfixed_handle:
		for filename in unfixed_handle:

			if os.path.exists(filename + '.xz.gpg'):
				print filename + '.xz.gpg'

			elif os.path.exists(filename + '.xz.gpg.save'):
				print filename + '.xz.gpg.save'

