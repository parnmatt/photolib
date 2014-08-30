#!/usr/bin/env python

from glob import glob
from os import chdir, remove, rename
from os.path import abspath, isdir, splitext
from sys import argv

from photolib import Photo

# Require only one directory
photo_dir = abspath(argv[1])
if (len(argv) != 2 or not isdir(photo_dir)):
    print "Pass only one existing directory"
    exit(1)

def get_images():
    image_exts = (".jpg", ".png")
    images = set(file
                 for file in glob("*")
                 if file.lower().endswith(image_exts))
    return images

def remove_files(file_list):
    for file in file_list:
        remove(file)

def rename_photos(photos):
    for photo in photos:
        rename(photo.filename, photo.prefered_filename())

chdir(photo_dir)
photo_files = get_images()

# Sort unique files from duplicates
photos = set(sorted([Photo(photo_file) for photo_file in photo_files]))
unique_photo_files = set(photo.filename for photo in photos)
duplicates = photo_files - unique_photo_files

remove_files(duplicates)
rename_photos(photos)
