#!/usr/bin/env python3

import csv
import os.path as path
import sys


class CSVFile:
    def __init__(self, file_name) -> None:
        self.file = open(file_name, newline="")
        self.reader = csv.reader(
            self.file, delimiter=",", quotechar='"', escapechar="\\"
        )
        self.columns = next(self.reader, None)

    def close(self):
        self.file.close()


def print_error(message):
    print(message, file=sys.stderr)


def process_file(writer, reader, base_name):
    for row in reader:
        row.append(base_name)
        writer.writerow(row)


def merge_files(files, writer=None):
    if writer is None:
        writer = csv.writer(
            sys.stdout,
            doublequote=False,
            escapechar="\\",
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
    columns = None
    for file in files:
        # Check that file exists
        if not path.isfile(file):
            print_error(f"Warning: file {file} does not exist. Ignoring file.")
            continue

        csv_file = CSVFile(file)
        # Check that file has same columns as the first file
        if columns and csv_file.columns != columns:
            print_error(
                f"Warning: file {file} has different columns than the first file. Ignoring file."
            )
            continue

        if columns is None:
            columns = csv_file.columns
            writer.writerow(columns + ["filename"])
        process_file(writer, csv_file.reader, path.basename(file))
        csv_file.close()


def main():
    if len(sys.argv) < 2:
        print_error("No files provided.\nUsage: python3 csvcombiner.py file1...")
        return
    merge_files(sys.argv[1:])


if __name__ == "__main__":
    main()
