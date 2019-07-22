#!/usr/bin/env python3
import os
import argparse
from datetime import datetime

def read_reference_timestamp_from_file(filename):
    with open(filename) as timestampfile:
        return datetime.strptime(timestampfile.read().strip(), "%Y-%m-%d %H:%M:%S")


def last_file_access_time(filename):
    """
    Get a datetime() representing the last access time of the given file.
    The returned datetime object is in local time
    """
    return datetime.fromtimestamp(os.stat(filename).st_atime)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from", help="The directory to copy from")
    parser.add_argument("to", help="The directory to copy to")
    args = parser.parse_args()

    # 
    reftime = read_reference_timestamp_from_file("copy-since-timestamp.txt")
    print(reftime)

    for subdir, dirs, files in os.walk(vars(args)["from"]):
        for file in files:
            filepath = os.path.abspath(os.path.join(subdir, file))
            atime = last_file_access_time(filepath)
            if atime < reftime:
                continue
            print(filepath)
