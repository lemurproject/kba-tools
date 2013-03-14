#!/usr/bin/env python

import os
import sys


if __name__ == '__main':
	original_dataset_directory = sys.argv[1]

	original_files = []
	gzipped = []

	for root, dirs, files in os.walk(original_dataset_directory):

		for filename in files:
			if filename.find('.xz.gpg.save') >= 0:
				original_files.append(os.path.join(root, filename.replace('.xz.gpg.save', '')))

			elif filename.find('.xz.gpg') >= 0:
				original_files.append(os.path.join(root, filename.replace('.xz.gpg', '')))

			elif filename.find('.gz') >= 0:
				gzipped.append(os.path.join(root, filename.replace('.gz', '')))

		for filename in original_files:
			if not filename in gzipped:
				print filename

		sys.stdout.flush()
		original_files = []
		gzipped = []

	for fname in original_files:
		if not fname in gzipped:
			print fname
