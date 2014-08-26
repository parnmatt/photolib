#!/usr/bin/env python

from glob import glob
from os import chdir, remove, rename
from os.path import abspath, isdir, splitext
from sys import argv

from photolib import Photo

# Require only one directory
photoDir = abspath(argv[1])
if (len(argv) != 2 or not isdir(photoDir)):
    print "Pass only one existing directory"
    exit(1)

def get_images():
    imageExts = [".jpg", ".png"]
    images = set()
    for file in glob("*"):
        ext = splitext(file)[-1]
        if (ext.lower() in imageExts):
            images.add(file)
    return images

def remove_files(fileList):
    for file in fileList:
        remove(file)

def rename_photos(photos):
    for photo in photos:
        rename(photo.filename, photo.prefered_filename())

chdir(photoDir)
photoFiles = get_images()

# Sort unique files from duplicates
photos = set(sorted([Photo(photoFile) for photoFile in photoFiles]))
uniquePhotoFiles = set(photo.filename for photo in photos)
duplicates = photoFiles - uniquePhotoFiles

remove_files(duplicates)
rename_photos(photos)
