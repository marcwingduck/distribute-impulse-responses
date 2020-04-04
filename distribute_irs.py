#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2017 Marc Lieser

import os
import argparse
from shutil import copyfile

n_banks = 10
n_presets = 10
n_irs = n_banks * n_presets


def silent_remove(filename):
    """Silently remove a file"""
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # no such file or directory
            raise


def create_dirs(drive):
    for i in range(n_banks):
        for j in range(n_presets):
            bank_str = "Bank_" + str(i)
            preset_str = "Preset_" + str(j)
            directory = os.path.join(drive, bank_str, preset_str)
            if not os.path.isdir(directory):
                os.makedirs(directory)


def distribute(collection, drive, skip):
    """Distribute the IR collection to the AMT Pangaea USB drive"""

    # collect IRs
    impulses = []
    for root, dirs, files in os.walk(collection):
        for name in sorted(files):
            impulses.append(os.path.join(root, name))

    c = 0
    for i in range(n_banks):
        # skip this bank if desired
        if i in skip:
            continue
        for j in range(n_presets):
            # more impulses than slots
            if c == len(impulses):
                break

            # current impulse
            impulse = impulses[c]

            bank_str = "Bank_" + str(i)
            preset_str = "Preset_" + str(j)
            directory = os.path.join(drive, bank_str, preset_str)

            # create if necessary
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # remove IRs located in directory
            for irname in os.listdir(directory):
                if irname.endswith('.wav'):
                    silent_remove(os.path.join(directory, irname))

            # copy current impulse
            print('Copying {} to {}... '.format(impulse, os.path.join(directory, os.path.basename(impulse))), end='')
            copyfile(impulse, os.path.join(directory, os.path.basename(impulse)))
            print('done.')

            # increment
            c += 1

    # print summary
    print('Copied {}/{} IRs.'.format(c, len(impulses)))


if __name__ == "__main__":
    # generate command line argument parser
    parser = argparse.ArgumentParser(description='Recursively distribute IRs from a given directory to the bank/preset directories of the AMT Pangaea IR Convolution Player CP-100.')

    # setup arguments
    parser.add_argument('-c', '--collection', help='Directory with IRs to distribute.', type=str, required=True)
    parser.add_argument('-d', '--drive', help='Path to the USB drive.', type=str, required=True)
    parser.add_argument('-s', '--skip', help='List of bank numbers to be skipped.', nargs='+', type=int, default=[])
    parser.add_argument('-b', '--build', help='Build directory structure and exit.', type=bool, default=False)

    # parse arguments
    args = parser.parse_args()

    if args.build:
        create_dirs(args.drive)
        exit(0)

    # generate pattern
    distribute(args.collection, args.drive, args.skip)
