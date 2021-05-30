"""
Author:         Decaff_42
Release Date:   04 September 2020
License:        CC BY-NC-SA
Version:        1.0
"""


class SRF:
    def __init__(self, raw):
        # No real processing should be needed here.
        self.raw = raw
        self.rows = len(raw)
        self.write = raw
        print(raw[0])
        self.name = raw[0].split('"')[1]
