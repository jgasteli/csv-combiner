import pytest
import csvcombiner
import os, csv

os.chdir("./tests")


def test_read_columns():
    file = csvcombiner.CSVFile("file1.csv")
    assert file.columns == ["email_hash", "category"]
    file.close()


def test_read_rows():
    file = csvcombiner.CSVFile("file1.csv")
    target = [
        ["b9f6f22276c919da793da65c76345ebb0b072257d12402107d09c89bc369a6b6", "Blouses"],
        ["c2b5fa9e09ef2464a2b9ed7e351a5e1499823083c057913c6995fdf4335c73e7", "Shirts"],
    ]
    i = 0
    for row in file.reader:
        assert row == target[i]
        i += 1
    assert i == len(target)
    file.close()


def test_merge_files():
    temp_path = "temp.csv"
    files = ["file1.csv", "file2.csv"]
    with open(temp_path, "w", newline="") as temp_file:
        writer = csv.writer(
            temp_file,
            doublequote=False,
            escapechar="\\",
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        csvcombiner.merge_files(files, writer=writer)

    with open(temp_path, "r") as temp_file:
        with open("filecombined.csv", "r") as target:
            assert temp_file.read() == target.read()
    os.remove(temp_path)
