#! /usr/bin/env python3

import os
import glob
from os import path
from distutils import dir_util
import subprocess
from multiprocessing import Pool, cpu_count

srcdir = 'pictures'
thread_count = cpu_count()
gallery_folders = [ name for name in os.listdir(srcdir) if path.isdir(path.join(srcdir, name)) ]

def read_quality(path):
	quality = subprocess.run(['identify', '-ping', '-format', '%Q', path], stdout=subprocess.PIPE)
	try:
		return int(quality.stdout)
	except:
		return 0

def read_width(path):
	width = subprocess.run(['identify', '-ping', '-format', '%w', path], stdout=subprocess.PIPE)
	try:
		return int(width.stdout)
	except:
		return 0

def scale_large(path):
	if read_quality(path) > 95:
		subprocess.run(['mogrify', '-monitor', '-quality', '95', path])
		return True
	return False

def scale_small(path):
	if read_quality(path) > 95 or read_width(path) > 600:
		subprocess.run(['mogrify', '-monitor', '-quality', '90', '-resize', '600x', path])
		return True
	return False

for folder in gallery_folders:
	src_path = path.join(srcdir, folder)
	target_path =  path.join('public', folder)
	small_target_path = path.join(target_path, 'small')
	large_target_path = path.join(target_path, 'large')

	print("\nSyncing {} to {}".format(src_path, target_path))
	subprocess.run(['rsync', '--recursive', '--delete', '--update', src_path + '/', small_target_path])
	subprocess.run(['ln', '-sf', '../../' + src_path, large_target_path])
	
	print("\nScaling {} ({} threads)".format(target_path, thread_count))

	do_zip = True
	with Pool(thread_count) as pool:
		large_pictures = glob.glob(path.join(large_target_path, '*'))
		results = pool.map(scale_large, large_pictures)

		small_pictures = glob.glob(path.join(small_target_path, '*'))
		results+= pool.map(scale_small, small_pictures)

		do_zip = any(results)

	zip_target_path = path.join(target_path, folder + '.zip')
	if (not path.exists(zip_target_path)) or do_zip:
		print("\nZipping {}".format(target_path))
		subprocess.run(['zip', '-j', '-r', zip_target_path, large_target_path])
