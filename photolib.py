#!/usr/bin/env python

__version__ = '0.1.0'

from datetime import datetime
from os.path import getctime, getsize, splitext
from PIL import Image
from PIL.ExifTags import TAGS
import string


def validFilename(filenameString):
    validChars = "-_.() " + string.ascii_letters + string.digits
    filename = "".join(c for c in filenameString if c in validChars)
    filename = filename.replace(" ", "_")
    return filename

class Photo:
    def __init__(self, filename):

        self.filename = filename
        self.size = getsize(filename)

        __tags = self.__getTags()
        self.width = __tags.get('ExifImageWidth', 0)
        self.height = __tags.get('ExifImageHeight', 0)
        self.datetime = self.__getDatetime(__tags)

    def __getTags(self):
        tags = {}
        image = Image.open(self.filename)
        if hasattr(image, "_getexif"):
            rawTags = image._getexif()
            if rawTags != None:
                tags = {TAGS.get(tag, tag): value
                            for tag, value in rawTags.items()}
        return tags

    # try metadata
    #   original, then digitised, then modified
    # finally if all failed, created time
    def __getDatetime(self, tags):
        dt =   tags.get('DateTimeOriginal'
             , tags.get('DateTimeDigitized'
             , tags.get('DateTime'
             , getctime(self.filename))))

        if type(dt) == str:
            dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        else:
            dt = datetime.fromtimestamp(dt)
        return dt


    def preferedFilename(self):
        ext = splitext(self.filename)[-1].lower()
        return validFilename(self.datetime.isoformat() + ext)

    def __cmp__(self, other):
        value = 0
        down = -1
        up = 1

        # earlier datetime
        if (self.datetime < other.datetime):
            value = down
        elif (self.datetime > other.datetime):
            value = up

        # large area
        elif (self.width * self.height > other.width * other.height):
            value = down
        elif (self.width * self.height < other.width * other.height):
            value = up

        # smaller filesize
        elif (self.size < other.size):
            value = down
        elif (self.size > other.size):
            value = up

        # alphanumerical
        elif (self.filename.lower() < other.filename.lower()):
            value = down
        elif (self.filename.lower() > other.filename.lower()):
            value = up

        return value

    # Photo tuple of unique objects
    def __key(self):
        return (self.datetime)

    def __eq__(x, y):
        return type(x) == type(y) and x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.filename)

    def __repr__(self):
        return repr({'filename': self.filename,
                    'width': self.width,
                    'height': self.height,
                    'datetime': self.datetime,
                    'size': self.size})
