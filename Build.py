#!/usr/bin/env python

from os import walk
from os.path import join
from zipfile import ZipFile

FILENAME_LIST = (
    "info.plist",
    "entry_point.py",
    "core.py",
)

PATH_LIST = (
    "arrow",
    "backports",
    "dateutil",
    "ualfred",
)


def main():
    with open("version") as f:
        version = f.readline().rstrip("\n\r ")

    zip_filename = f"time-converter.{version}.alfredworkflow"
    z = ZipFile(zip_filename, mode="w")

    for filename in FILENAME_LIST:
        z.write(filename)

    for pathname in PATH_LIST:
        for root, dirs, files in walk(pathname):
            for filename in files:
                if filename.rfind(".pyc") == -1:
                    z.write(join(root, filename))

    z.close()

    print(f"Create Alfred workflow({zip_filename}) finished.")


if __name__ == "__main__":
    main()
