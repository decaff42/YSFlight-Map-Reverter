"""
Author:         Decaff_42
Release Date:   04 September 2020
License:        CC BY-NC-SA
Version:        1.0
"""


def import_fld(f_path):
    """Import a formatted text file"""
    with open(f_path, 'r') as fld_file:
        data = fld_file.read().splitlines()

    # Remove the \n characters from the end of each row.
    for row, line in enumerate(data):
        if line.endswith("\n"):
            data[row] = line[:-1]

    return data


def write_fld(f_path, data):
    """Write a formatted text file"""

    # Check filename
    if f_path.endswith(".fld") is False:
        f_path = f_path + ".fld"

    with open(f_path, 'w') as fld_file:
        for line in data:
            fld_file.write(line + '\n')
