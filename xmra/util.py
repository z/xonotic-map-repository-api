import os
import sys
import time
import json
import hashlib
from shutil import copyfile
from datetime import datetime


def replace_last(s, old, new):
    return s[::-1].replace(old[::-1], new[::-1], 1)[::-1]


def reporthook(count, block_size, total_size):

    global start_time

    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed. " %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def check_if_not_create(file, template):
    if not os.path.isfile(file):
        try:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            copyfile(template, file)
        except OSError:
            raise SystemExit


def hash_file(filename):
    """This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename,'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


class ObjectEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that leverages an object's `__json__()` method,
    if available, to obtain its default JSON representation.
    http://stackoverflow.com/a/24030569
    """
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

