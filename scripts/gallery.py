#! /usr/bin/env python3

import os
import glob
from os import path
from distutils import dir_util
import subprocess
from multiprocessing import Pool

srcdir = 'pictures'
thread_count = 8
gallery_folders = [ name for name in os.listdir(srcdir) if path.isdir(path.join(srcdir, name)) ]

def scale_large(path):
	subprocess.run(['mogrify', '-monitor', '-quality', '95', path])

def scale_small(path):
	subprocess.run(['mogrify', '-monitor', '-quality', '90', '-resize', 'x600', path])

for folder in gallery_folders:
	src_path = path.join(srcdir, folder)
	target_path =  path.join('public', folder)
	small_target_path = path.join(target_path, 'small')
	large_target_path = path.join(target_path, 'large')

	print("\nCopying {} to {}".format(src_path, target_path))
	dir_util.copy_tree(src_path, small_target_path)
	dir_util.copy_tree(src_path, large_target_path)
	
	print("\nScaling {}".format(target_path))

	with Pool(thread_count) as pool:
		large_pictures = glob.glob(path.join(large_target_path, '*'))
		pool.map(scale_large, large_pictures)

		small_pictures = glob.glob(path.join(small_target_path, '*'))
		pool.map(scale_small, small_pictures)

	print("\nZipping {}".format(target_path))
	subprocess.run(['zip', '-j', '-r', path.join(target_path, folder + '.zip'), large_target_path])
