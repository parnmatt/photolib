#!/usr/bin/env python

__version__ = '1.0.0'

from datetime import datetime
from os.path import getctime, getsize, splitext
from PIL import Image
from PIL.ExifTags import TAGS
import string


def valid_filename(filenameString):
    validChars = "-_.() " + string.ascii_letters + string.digits
    filename = "".join(c for c in filenameString if c in validChars)
    filename = filename.replace(" ", "_")
    return filename

class Photo:
    def __init__(self, filename):

        self.filename = filename
        self._size = getsize(filename)

        self._tags = self._get_tags()
        self._width = self._tags.get('ExifImageWidth', 0)
        self._height = self. _tags.get('ExifImageHeight', 0)
        self._datetime = self._get_datetime()

    def _get_tags(self):
        tags = {}
        image = Image.open(self.filename)
        if hasattr(image, "_getexif"):
            rawTags = image._getexif()
            if rawTags is not None:
                tags = {TAGS.get(tag, tag): value
                            for tag, value in rawTags.items()}
        return tags

    # try metadata
    #   original, then digitised, then modified
    # finally if all failed, created time
    def _get_datetime(self):
        dt =   self._tags.get('DateTimeOriginal'
             , self._tags.get('DateTimeDigitized'
             , self._tags.get('DateTime'
             , getctime(self.filename))))

        if isinstance(dt, basestring):
            dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        else:
            dt = datetime.fromtimestamp(dt)
        return dt


    def prefered_filename(self):
        ext = splitext(self.filename)[-1].lower()
        return valid_filename(self._datetime.isoformat() + ext)

    def __cmp__(self, other):
        value = 0
        down = -1
        up = 1

        # earlier datetime
        if (self._datetime < other._datetime):
            value = down
        elif (self._datetime > other._datetime):
            value = up

        # large area
        elif (self._width * self._height > other._width * other._height):
            value = down
        elif (self._width * self._height < other._width * other._height):
            value = up

        # smaller filesize
        elif (self._size < other._size):
            value = down
        elif (self._size > other._size):
            value = up

        # alphanumerical
        elif (self.filename.lower() < other.filename.lower()):
            value = down
        elif (self.filename.lower() > other.filename.lower()):
            value = up

        return value

    # Photo tuple of unique objects
    def __key(self):
        return (self._datetime)

    def __eq__(x, y):
        return isinstance(x, y) and x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    def __str__(self):
        return str(self.filename)

    def __repr__(self):
        return repr({'filename': self.filename,
                    'width': self._width,
                    'height': self._height,
                    'datetime': self._datetime,
                    'size': self._size})
