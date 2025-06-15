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
    file_paths = recLister(args.root_folder)
    with open(args.csv_dest+"output.csv","w") as output:
        for file_path in file_paths:
            split = os.path.split(file_path)
            output.write(split[0]+", "+split[1]+"\n")


def recLister(root_path):
    directories = os.listdir(root_path)
    ret_value = []

    for item in directories:
        if os.path.isdir(os.path.join(root_path, item)):
            dir_files = recLister(os.path.join(root_path, item))
            for file in dir_files:
                ret_value.append(os.path.join(item, file))
        elif os.path.isfile(os.path.join(root_path, item)):
            ret_value.append(item)

    return ret_value


if __name__ == "__main__":
    app.run(main, flags_parser=parse_args)