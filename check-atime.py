#!/usr/bin/env python3
"""
This utility script checks which atime mode (always-update on access, relatime or noatime)
is in use for the current filesystem
"""
import os
import time
from datetime import datetime

def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond/1e6

def set_file_access_time(filename, atime):
    """
    Set the access time of a given filename to the given atime.
    atime must be a datetime object.
    """
    stat = os.stat(filename)
    mtime = stat.st_mtime
    os.utime(filename, times=(datetime_to_timestamp(atime), mtime))


def last_file_access_time(filename):
    """
    Get a datetime() representing the last access time of the given file.
    The returned datetime object is in local time
    """
    return datetime.fromtimestamp(os.stat(filename).st_atime)

try:
    # Create test file
    with open("test.txt", "w") as outfile:
        outfile.write("test!")
    time.sleep(0.1)
    # Read & get first atime
    with open("test.txt") as infile:
        infile.read()
    atime1 = last_file_access_time("test.txt")
    # Now read file
    time.sleep(0.1)
    with open("test.txt") as infile:
        infile.read()
    # Different atime after read?
    atime2 = last_file_access_time("test.txt")
    # Set OLD atime for relatime check!
    set_file_access_time("test.txt", datetime(2000, 1, 1, 0, 0, 0))
    # Access again
    with open("test.txt") as infile:
        infile.read()
    # Different atime now
    atime3 = last_file_access_time("test.txt")
    # Check atime
    changed_after_simple_access = atime2 > atime1
    changed_after_old_atime = atime3 > atime1
    # Convert mode to text and print
    if (not changed_after_simple_access) and (not changed_after_old_atime):
        print("Your filesystem is mounted in NOATIME mode - access times will NEVER be updated automatically")
    elif (not changed_after_simple_access) and changed_after_old_atime:
        print("Your filesystem is mounted in RELATIME mode - access times will only be updated if they are too old")
    elif changed_after_simple_access and (not changed_after_old_atime):
        print("Unable to determine your access time mode")
    else: # Both updated
        print("Your filesystem is mounted in ATIME mode - access times will be updated on EVERY file access")
finally:
    # Delete our test file
    try:
        os.remove("test.txt")
    except:
        pass