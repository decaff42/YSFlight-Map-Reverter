"""
Author:         Decaff_42
Release Date:   04 September 2020
License:        CC BY-NC-SA
Version:        1.0
"""


class TER:
    def __init__(self, raw):
        self.raw = raw
        self.rows = len(raw)
        self.write = list()
        self.name = raw[0].split('"')[1]

        # Run the function to handle the details.
        self.process()

    def process(self):
        """Search for items in the raw data that need to be removed and remove them."""
        raw = self.raw  # Bring in as local to prevent distorting the class-stored raw parameter
        lines_to_delete = list()

        # Identify and record lines that need to be handled
        for row, line in enumerate(raw):
            if line.startswith("SPEC") or line.startswith("TEX MAIN"):
                lines_to_delete.append(row)

        # Delete the raw data elements
        lines_to_delete = list(set(lines_to_delete))
        lines_to_delete.sort(reverse=True)  # Reverse order so the delete is always working on an accurate index
        for row in lines_to_delete:
            del raw[row]

        # Update the row count in the first line of the elevation grid definition
        self.rows = len(raw)
        header = raw[0].split(" ")
        header[-1] = str(self.rows)  # Overwrite with new row count
        header = " ".join(header)
        raw[0] = header

        # Store processed data as write
        self.write = raw
