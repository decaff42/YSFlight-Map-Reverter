"""
Author:         Decaff_42
Release Date:   04 September 2020
License:        CC BY-NC-SA
Version:        1.0
"""

from lib.class_pc2 import PC2
from lib.class_srf import SRF
from lib.class_ter import TER


class FLD:
    def __init__(self, raw):
        self.raw = raw
        self.rows = len(raw)
        self.data = list()
        self.header = list()
        self.tail = list()
        self.elements = list()
        self.internal_elements = list()
        self.element_types = list()

        # Next row that we can start looking for elements.
        # Needs to be greater than zero so internal .fld definitions don't recursively make child classes
        self.resume_row = 1

        # Need to account for the main FLD not having the PCK line in front of the FIELD row
        if raw[0].startswith("PCK") is True:
            self.name = raw[0].split('"')[1]
        else:
            self.name = "Main FLD"
            print(" ")
        print("FLD: {} ... Length: {}".format(self.name, self.rows))

        # Run the processing required.
        self.process_header()  # Removes all bad parts from the header
        self.process_elements()
        self.process_tail()

        # Compile the FLD with alterations made.
        self.write = self.header + self.internal_elements + self.tail

        # Adjust the row count if this is an internally-defined .fld element.
        if self.write[0].startswith("PCK"):
            # Update the row count in the first line of the fld grid definition
            self.rows = len(self.write)
            header = self.write[0].split(" ")
            header[-1] = str(self.rows)  # Overwrite with new row count
            header = " ".join(header)
            self.write[0] = header

    def process_elements(self):
        elements = list()  # List of class instances
        element_types = list()
        self.resume_row = 1

        # Iterate through the raw data to find the internally defined components.
        for row_num, line in enumerate(self.raw):
            if line.startswith("PCK") and row_num >= self.resume_row:
                # This is the start of an internal element that needs to be accounted for.
                element_row_count = int(line.split(" ")[-1])
                self.resume_row = row_num + element_row_count
                element = self.raw[row_num:self.resume_row]
                # Figure out what kind of element this is and create appropriate classes.
                file_type = element[0].split('"')[1][-4:]
                element_data = None
                if file_type == ".ter":
                    element_data = TER(element)
                    element_types.append("ter")
                elif file_type == ".fld":
                    element_data = FLD(element)
                    element_types.append("fld")
                elif file_type == ".pc2":
                    element_data = PC2(element)
                    element_types.append("pc2")
                elif file_type == ".srf":
                    element_data = SRF(element)
                    element_types.append("srf")
                print("Element: {} ... Length: {}".format(element_data.name, len(element)))
                element_data = element_data.write
                elements.append(element_data)

        # Store the class instances
        self.elements = elements
        self.element_types = element_types

        # write the results of the class instances.
        for elem in self.elements:
            self.internal_elements.extend(elem)
            for i in range(3):
                self.internal_elements.append("")

    def process_tail(self):
        """Take care of all the tail of the FLD where elements are positioned."""
        # Tail starts with the resume_row and goes to end of file.
        need_to_remove = False
        lines_to_remove = list()
        tail = self.raw[self.resume_row:]

        for row, line in enumerate(tail):
            if line.startswith("AOB") and need_to_remove is False:
                need_to_remove = True

            if need_to_remove is True:
                lines_to_remove.append(row)

            if line.startswith("END") and need_to_remove is True:
                need_to_remove = False

        # # Reset high flag numbers that player controlled ground objects seem to use.
        # # Use FLG 0 as a safe item.
        # for row, line in enumerate(tail):
        #     if line.startswith("FLG"):
        #         num = int(line.split()[-1])
        #         if num > 7:
        #             tail[row] = "FLG 0"

        # Delete the bad lines
        lines_to_remove.reverse()
        for row in lines_to_remove:
            del tail[row]

        self.tail = tail

    def process_header(self):
        header = list()
        for row, line in enumerate(self.raw):
            if line.startswith("PCK") and row > 0:
                break
            header.append(line)

        # Remove bad lines that start with easy prefix
        lines_to_delete = list()
        for row, line in enumerate(header):
            if (line.startswith("FLDVERSION") or line.startswith("FLDNAME") or line.startswith("GNDSPECULAR") or
                    line.startswith("BASEELV") or line.startswith("MAGVAR") or line.startswith("CANRESUME") or
                    line.startswith("TEXMAN")):
                lines_to_delete.append(row)

        # Identify Air Route groups. Bounded by AIRROUTE and ENDAIRROUTE rows
        air_route = False
        for row, line in enumerate(header):
            if line.startswith("AIRROUTE") and air_route is False:
                air_route = True

            if line.startswith("ENDAIRROUTE") and air_route is True:
                lines_to_delete.append(row)

            if air_route is True:
                lines_to_delete.append(row)

        # Delete the bad lines
        lines_to_delete = list(set(lines_to_delete))
        lines_to_delete.sort(reverse=True)
        for row in lines_to_delete:
            del header[row]

        self.header = header
