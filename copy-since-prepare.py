#!/usr/bin/env python3
from datetime import datetime
import os
import argparse

def write_reference_timestamp_to_file(filename):
    with open(filename, "w") as timestampfile:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestampfile.write(now)

def set_file_access_time(filename, atime):
    """
    Set the access time of a given filename to the given atime.
    atime must be a datetime object.
    """
    stat = os.stat(filename)
    mtime = stat.st_mtime
    os.utime(filename, times=(atime.timestamp(), mtime))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="The directory to copy from")
    parser.add_argument("-c", "--compatibility", action="store_true", help="Compatibility mode (for relatime)")
    args = parser.parse_args()

    write_reference_timestamp_to_file("copy-since-timestamp.txt")

    if args.compatibility:
        # Set "really old" access time on all those files
        # This forces "relatime"-style mounted filesystems to update on access!
        atime = datetime(2000, 1, 1, 0, 0, 0)
        for subdir, dirs, files in os.walk(args.source):
            for directory in dirs:
                set_file_access_time(os.path.join(subdir, directory), atime)
            for file in files:
                set_file_access_time(os.path.join(subdir, file), atime)
            set_file_access_time(os.path.join(subdir), atime)
