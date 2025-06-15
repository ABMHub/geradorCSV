import os
import argparse

from absl import app
from absl.flags import argparse_flags

def parse_args(argv):
    parser = argparse_flags.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--root_folder",
        type=str,
        help="Folder to start cataloguing the files from.",
        default="./"
    )
    parser.add_argument(
        "--csv_dest",
        type=str,
        help="Folder to output the CSV.",
        default="./"
    )
    args = parser.parse_args(argv[1:])
    return args

def main(args):
    filePaths = recLister(args.root_folder)
    with open(args.csv_dest+"output.csv","w") as output:
        for filePath in filePaths:
            split = os.path.split(filePath)
            output.write(split[0]+", "+split[1]+"\n")


def recLister(rootPath):
    directories = os.listdir(rootPath)
    retValue = []

    for item in directories:
        if os.path.isdir(os.path.join(rootPath, item)):
            dirFiles = recLister(os.path.join(rootPath, item))
            for file in dirFiles:
                retValue.append(os.path.join(item, file))
        elif os.path.isfile(os.path.join(rootPath, item)):
            retValue.append(item)

    return retValue


if __name__ == "__main__":
    app.run(main, flags_parser=parse_args)