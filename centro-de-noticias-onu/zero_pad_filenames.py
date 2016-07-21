#!/usr/bin/python
import argparse
import glob, os

parser = argparse.ArgumentParser(description='Zero pad the file names in a directory to 5 digits')
parser.add_argument('dir', type=str,  help='directory containing files')
args = parser.parse_args()

for file in glob.glob(args.dir + "\*"):
    base = os.path.basename(file)
    name = os.path.splitext(base)
    if (len(name[0]) < 5):
        new_file = args.dir + "\\" + name[0].zfill(5) + name[1]
        print("move " + file + " to " + new_file)
        os.rename(file, new_file)
