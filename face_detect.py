#!/usr/bin/python
# face_detect.py
# Face Detection using OpenCV. Based on script at:
# http://creatingwithcode.com/howto/face-detection-in-static-images-with-python/
# Usage: python face_detect.py [image filename]

import sys,os
from opencv.cv import *
from opencv.highgui import *
from PIL import Image, ImageOps

CLASSIFIER = '/usr/share/doc/opencv-doc/examples/haarcascades/haarcascade_frontalface_default.xml'
CROP_DIR = '/home/tim/mycode/recordsearch/src/recordsearchtools/files/crops'

def detect_objects(fn, image):
	"""Detects faces and then crops the image."""
	#grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
	#cvCvtColor(image, grayscale, CV_BGR2GRAY)

	storage = cvCreateMemStorage(0)
	cvClearMemStorage(storage)
	#cvEqualizeHist(grayscale, grayscale)
	cascade = cvLoadHaarClassifierCascade(CLASSIFIER, cvSize(1,1))
	faces = cvHaarDetectObjects(image, cascade, storage, 1.3, 3, CV_HAAR_DO_CANNY_PRUNING, cvSize(20,20))
	if faces:
		i = 1
		for f in faces:
			#newfn = fn + ".output.jpg"
			#os.system("convert %s -stroke red -fill none -draw 'rectangle %d,%d %d,%d' %s" % (fn, f.x, f.y, f.x+f.width, f.y+f.height, newfn))
			#os.system("mv %s %s.orig" % (fn, fn))
			#os.system("mv %s %s" % (newfn, fn))
			#print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
			file, ext = os.path.splitext(fn)
			im = Image.open(fn)
			# Increase selected area by 50px on each side then crop
			im = im.crop((f.x-50, f.y-50, f.x+f.width+50, f.y+f.height+50))
			# Minor contrast adjustment
			im = ImageOps.autocontrast(im, cutoff=0.5)
			im.load()
			crop = '%s/%s_crop_%s.jpg' % (CROP_DIR, os.path.basename(file), i)
			im.save(crop, "JPEG")
			check_crop(crop)
			i += 1
		
def check_crop(crop):
	"""Try to reduce false positives by doing a second pass and deleting images that fail."""
	image = cvLoadImage(crop);
	storage = cvCreateMemStorage(0)
	cvClearMemStorage(storage)
	cascade = cvLoadHaarClassifierCascade(CLASSIFIER, cvSize(1,1))
	faces = cvHaarDetectObjects(image, cascade, storage, 1.3, 3, CV_HAAR_DO_CANNY_PRUNING, cvSize(20,20))
	if faces:
		if faces[0] is None:
			os.remove(crop)
	else:
		os.remove(crop)

def process_image(fn):
	image = cvLoadImage(fn);
	detect_objects(fn, image)

def main():
	image = cvLoadImage(sys.argv[1]);
	detect_objects(sys.argv[1], image)

if __name__ == "__main__":
	main()
