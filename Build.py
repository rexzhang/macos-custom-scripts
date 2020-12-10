#!/usr/bin/python
# encoding: utf-8

from os import walk
from os.path import join
from zipfile import ZipFile

FILENAME_LIST = (
    'info.plist',

    'entry_point.py',
    'core.py',

)

PATH_LIST = (
    'workflow',
    'arrow',
    'backports',
    'dateutil',
)


def main():
    with open('version') as f:
        version = f.readline().rstrip('\n\r ')

    zip_filename = 'time-converter.{}.alfredworkflow'.format(version)
    z = ZipFile(zip_filename, mode='w')

    for filename in FILENAME_LIST:
        z.write(filename)

    for pathname in PATH_LIST:
        for root, dirs, files in walk(pathname):
            for filename in files:
                if filename.rfind('.pyc') == -1:
                    z.write(join(root, filename))

    z.close()

    print('Create Alfred workflow({}) finished.'.format(zip_filename))


if __name__ == '__main__':
    main()
