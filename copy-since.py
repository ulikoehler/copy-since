#!/usr/bin/env python3
import os
import shutil
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
    parser.add_argument("to", nargs="?", help="The directory to copy to")
    args = parser.parse_args()

    # 
    reftime = read_reference_timestamp_from_file("copy-since-timestamp.txt")

    fromdir = vars(args)["from"]
    for subdir, dirs, files in os.walk(fromdir):
        for file in files:
            abspath = os.path.abspath(os.path.join(subdir, file))
            if not os.path.isfile(abspath):
                continue
            # Skip copying if file has not been accessed
            atime = last_file_access_time(abspath)
            if atime < reftime:
                continue
            # Copy file if enabled
            relpath = os.path.relpath(abspath, start=fromdir)
            if args.to: # if we should copy
                dstpath = os.path.join(args.to, relpath)
                # Create dst directory if doesnt exist
                dstdir = os.path.dirname(dstpath)
                os.makedirs(dstdir, exist_ok=True)
                # Copy file (try to conserve metadata)
                shutil.copy2(abspath, dstpath)
                print('Copied {} to {}'.format(relpath, dstpath))
            else: # we wont copy => just print
                print(relpath)
