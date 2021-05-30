"""
Author:         Decaff_42
Release Date:   04 September 2020
License:        CC BY-NC-SA
Version:        1.0


FLD 2 OLD
This tool converts scenery files (.fld) from newer versions of YSFlight and YSFlight Scenery Editor (2009 through 2018)
and makes them compatible with Scenery Editor 2009 and thus all versions of YSFlight active in the community.

Many thanks to Waspe414 (UltraViolet) for helping with knowledge, support and testing. Thanks to Turbofan for help with
testing the code output.


INSTRUCTIONS:
(1) Open FLD2OLD.py
(2) Copy maps that should be reverted to 2009 standard into "Input Maps"
(3) Press F5
(4) Take Map from "Output Maps"
"""


# Import standard Python Modules
import os

# Import custom modules
from lib.func_import_export import import_fld, write_fld
from lib.class_fld import FLD


def run_all():
    """Control all the functions needed to perform the conversion."""
    fld_files = get_fld_files()

    for file in fld_files:
        # Import and parse the raw data
        print(os.path.basename(file))
        raw_fld = import_fld(file)
        fld = FLD(raw_fld)

        data = fld.write
        filename = os.path.basename(file)

        output_path = os.path.join(os.getcwd(), 'Output Maps', filename)

        write_fld(output_path, data)


def get_fld_files():
    """Get a list of all the .fld files in the input folder"""
    input_fld_path = os.path.join(os.getcwd(), 'Input Maps')
    fld_files = list()

    for path, subdir, files in os.walk(input_fld_path):
        for name in files:
            if name.endswith(".fld"):
                fld_files.append(os.path.join(path, name))

    return fld_files


run_all()
