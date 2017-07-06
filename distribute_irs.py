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


def distribute(collection, drive, skip):
    """Distribute the IR collection to the AMT Pangaea USB drive"""

    # collect IRs
    impulses = []
    for root, dirs, files in os.walk(collection):
        for name in sorted(files):
            impulses.append(os.path.join(root, name))

    n_skip = skip * n_banks  # number of presets to skip
    c = n_skip  # start index (skip first bank by default)

    for impulse in impulses:

        # more impulses than slots
        if c == n_irs - n_skip:
            break

        bank = c / n_banks  # bank number
        preset = c % n_presets  # preset number

        # generate directory names and join directory path
        bank_str = "Bank_" + str(bank)
        preset_str = "Preset_" + str(preset)
        directory = os.path.join(drive, bank_str, preset_str)

        # if not os.path.isdir(directory):
        #    os.makedirs(directory)

        # remove IRs located in directory
        for irname in os.listdir(directory):
            if irname.endswith('.wav'):
                silent_remove(os.path.join(directory, irname))

        # copy current impulse
        print 'Copying "%s" to "%s"...' % (impulse, os.path.join(directory, os.path.basename(impulse)))
        copyfile(impulse, os.path.join(directory, os.path.basename(impulse)))

        # increment
        c += 1

    # print summary
    print 'Copied %d/%d IRs.' % (c - n_skip, len(impulses))


if __name__ == "__main__":
    # generate command line argument parser
    parser = argparse.ArgumentParser(description='Recursively distribute IRs from a given directory to the bank/preset directories of the AMT Pangaea IR Convolution Player CP-100.')

    # setup arguments
    parser.add_argument('-c', '--collection', help='Directory with IRs to distribute.', type=str, required=True)
    parser.add_argument('-d', '--drive', help='Path to the USB drive.', type=str, required=True)
    parser.add_argument('-s', '--skip', help='Number of banks to skip.', nargs='?', const=1, type=int, default=1)

    # parse arguments
    args = parser.parse_args()

    # generate pattern
    distribute(args.collection, args.drive, args.skip)
