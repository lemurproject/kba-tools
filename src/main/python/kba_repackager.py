'''
Script to repackage KBA dataset
'''

import argparse
import os

def handle_files(kba_data_location, prefix_str, output_dir):
	files_to_cat = { 'social' : [], 'news' : [], 'linking' : []}
	for root, dirs, files in os.walk(kba_data_location):
		for filename in files:
			if filename.endswith('.gz') and root.find(prefix_str) >= 0:
				abs_path = os.path.abspath(os.path.join(root, filename))
				if filename.find('social') >= 0:
					files_to_cat['social'].append((abs_path, os.path.getsize(abs_path)))
				elif filename.find('news') >= 0:
					files_to_cat['news'].append((abs_path, os.path.getsize(abs_path)))
				elif filename.find('linking') >= 0:
					files_to_cat['linking'].append((abs_path, os.path.getsize(abs_path)))
	#print files_to_cat
	print 'social: ' + reduce(lambda (x, y) : x[1] + y[1], files_to_cat['social'])
	print 'news: ' + reduce(lambda (x, y) : x[1] + y[1], files_to_cat['news'])
	print 'lining: ' + reduce(lambda (x, y) : x[1] + y[1], files_to_cat['linking'])

if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()
		parser.add_argument(
			'kba_data_location',
			metavar = 'kba-data-location',
			help = 'location of current KBA data'
		)
		parser.add_argument(
			'prefix_str', 
			metavar = 'prefix-str', 
			help = 'Prefix of the type 2011-10-01. This will be a sub-dir I will create with the contents from current KBA data')
		parser.add_argument(
			'output_dir',
			metavar = 'output-dir',
			help = 'The sub-folders and files will be placed in here.'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	handle_files(parsed.kba_data_location, parsed.prefix_str, parsed.output_dir)
