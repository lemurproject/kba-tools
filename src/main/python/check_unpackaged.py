#!/usr/bin/env python

import os
import sys


if __name__ == '__main':
	files_list = sys.argv[1]

	original_files = []
	gzipped = []

	with open(files_list, 'r') as files_list_handle:
		for new_filename in files_list_handle:
			new_filename = new_filename.strip()

			if new_filename.find('.xz.gpg') >= 0:
				original_files.append(new_filename.replace('.xz.gpg', ''))

			elif new_filename.find('.gz') >= 0:
				original_files.append(new_filename.replace('.gz', ''))

	for fname in original_files:
		if not fname in gzipped:
			print fname
