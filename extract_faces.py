#!/usr/bin/python
# Loop through images and feed to facial detection script

import os
import face_detect

#rootdir = "/home/tim/mycode/recordsearch/src/recordsearchtools/files/E752"
rootdir = "/home/tim/mycode/recordsearch/src/recordsearchtools/files/ST84-1"
#rootdir = "/home/tim/mycode/recordsearch/src/recordsearchtools/files/test"
#rootdir = "/home/tim/mycode/recordsearch/src/recordsearchtools/files/ST84-1/1907-391-400-[1731871]"

for root, dirs, files in os.walk(rootdir, topdown=True):
	for file in files:
		print 'Processing %s' % file
		face_detect.process_image(os.path.join(root, file))
