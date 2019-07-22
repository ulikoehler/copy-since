# copy-since

Copy only files that have been accessed since a certain point in time.

### Why?

If you have a huge source tree including e.g. a full version of [boost](https://www.boost.org), you might need to extract only those files that you actually need for your project.

Instead of manually copying files and checking for compiler errors

### Requirements

* Python
* You file system must not have access times disabled (i.e. it won't work with `noatime` on Linux - `relatime` will work fine)

In case you are running a Linux-based system, an alternative to `copy-since` is [`selective-copy`](https://github.com/ulikoehler/selective-copy) which uses `open()` syscall hijacking and hence does not depend on filesystem access times being enabled.

### Usage

*copy-since* needs two pararameters: A *source* directory where the files will be read from and a *target* directory where the files will be copied to (the target directory is automatically created if it does not exist).

First, run the prepare script
```sh
./copy-since-prepare.py <source directory>
```

Any file accessed (read or write) after the call to `copy-since-prepare.py` will be copied later, so now you need to run your build / software etc. **Be sure to run a clean build (e.g. `make clean && make`) so all required files will be accessed!**

Now run the main copy script:

```sh
./copy-since-prepare.py <source directory> <target directory>
```

### How does it work?

`copy-since.py` is a simple access-time-threshold based copying script. `copy-since-prepare.py` however contains some additional logic that might not be obvious at first glance.

`copy-since-prepare.py` first writes the current timestamp to `copy-since-timestamp.txt` so `copy-since.py` will later know from which access timestamp to start copying files. However, `copy-since-prepare.py` will also manually set the access time of all files and directories.

This is relevant mostly if using `relatime` on Linux - `relatime`-mounted filesystems will only update the access times if it either:
* is older than the modification date or
* has not been changed for a predefined amount of time (e.g. 1 day for RHEL)

`copy-since-prepare.py` will force the access time to `2000-1-1` and hence force the latter condition to be true in any case, thereby forcing an update of the `atime` on file access.