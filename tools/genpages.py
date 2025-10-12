#!/usr/bin/env python
#
# Python program to generate page numbers for ARGUS/MITIGUS format sources.
#
# Jim Lawton 2016-11-14
#
# This assumes the presence of an "L" log section card in the file, and uses it
# to generate annotation comments with page numbers to ease the transcription
# process.

import argparse
import os
import os.path
import sys

import h800.arguscard


def main():
    parser = argparse.ArgumentParser(
        prog="genpages",
        description="Generate annotated page number cards for ARGUS assembly sources.",
    )
    parser.add_argument(
        "filename",
        help="ARGUS source file to annotate with page header/page number cards.",
    )
    args = parser.parse_args()

    filename = args.filename

    if not os.path.exists(filename):
        parser.error(f"Filename {filename} does not exist!")
        sys.exit(1)

    inlines = []
    with open(filename) as f:
        inlines = f.readlines()

    d = h800.arguscard.Deck(inlines)

    logsection = d.log_section
    logsectioncol8 = d.log_section_col8

    for line in inlines:
        if logsection is None:
            if line.startswith("# Filename: "):
                infilename = line.split()[2].strip()
                if "." in infilename:
                    infilename = infilename[: infilename.index(".")]
                logsection = infilename.replace("_", " ")
                logsectioncol8 = "@"
        if line.startswith("# Pages: "):
            page_range = line.split()[2].strip()
            if "-" in page_range:
                start = int(page_range.split("-")[0])
                end = int(page_range.split("-")[1])
            else:
                start = end = int(page_range)

    if logsection is None:
        parser.error("Cannot determine log section!")
        sys.exit(1)

    if start > end:
        parser.error("Invalid page numbers!")
        sys.exit(1)

    _numdigits = len(str(end))

    outlines = []
    outlines.append("\n")
    outlines.append(f"L      {logsectioncol8}{logsection}\n")
    for pagenum in range(start, end + 1):
        outlines.append("\n")
        outlines.append(f"# Page {pagenum}\n")
        outlines.append(
            f"#      {logsectioncol8}{logsection:-72s} USER'S OWN PAGE NO.{pagenum - start + 1:4s}        PAGE{pagenum - start + 1:4s}\n"
        )
        outlines.append("\n")

    with open(filename, "a") as f:
        f.writelines(outlines)


if __name__ == "__main__":
    main()
