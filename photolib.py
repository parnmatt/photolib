#!/usr/bin/env python

__version__ = '2.0.0'

from datetime import datetime
from os.path import getctime, getsize, splitext
from PIL import Image
from PIL.ExifTags import TAGS
import string


def valid_filename(filename_string):
    valid_chars = "-_.() " + string.ascii_letters + string.digits
    filename = "".join(c for c in filename_string if c in valid_chars)
    filename = filename.replace(" ", "_")
    return filename

class Photo:
    def __init__(self, filename):

        self.filename = filename
        self.size = getsize(filename)

        _tags = self._get_tags()
        self.width = _tags.get('ExifImageWidth', 0)
        self.height = _tags.get('ExifImageHeight', 0)
        self.datetime = self._get_datetime(_tags)

    def _get_tags(self):
        tags = {}
        image = Image.open(self.filename)
        if hasattr(image, "_getexif"):
            raw_tags = image._getexif()
            if raw_tags is not None:
                tags = {TAGS.get(tag, tag): value
                            for tag, value in raw_tags.items()}
        return tags

    # try metadata
    #   original, then digitised, then modified
    # finally if all failed, created time
    def _get_datetime(self, tags):
        dt = tags.get('DateTimeOriginal',
                tags.get('DateTimeDigitized',
                    tags.get('DateTime',
                        getctime(self.filename))))

        if isinstance(dt, str):
            dt = datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
        else:
            dt = datetime.fromtimestamp(dt)
        return dt


    def prefered_filename(self):
        _, ext = splitext(self.filename)
        ext = ext.lower()
        return valid_filename(self.datetime.isoformat() + ext)

    def __lt__(self, other):
        lt = False

        # earlier datetime
        lt |= self.datetime < other.datetime

        # large area
        lt |= self.width * self.height > other.width * other.height

        # smaller filesize
        lt |= self.size < other.size

        # alphanumerical
        lt |= self.filename.lower() < other.filename.lower()

        return lt

    # Photo tuple of unique objects
    def _key(self):
        return self.datetime,

    def __eq__(x, y):
        return type(x) == type(y) and x._key() == y._key()

    def __hash__(self):
        return hash(self._key())

    def __str__(self):
        return str(self.filename)

    def __repr__(self):
        return repr({'filename': self.filename,
                     'width': self.width,
                     'height': self.height,
                     'datetime': self.datetime,
                     'size': self.size,
                     })
