#!/usr/bin/env python
#
# Python program to generate page numbers for ARGUS/MITIGUS format sources.
#
# Jim Lawton 2016-11-14
#
# This assumes the presence of an "L" log section card in the file, and uses it
# to generate annotation comments with page numbers to ease the transcription
# process.

import sys
import os
import os.path
from optparse import OptionParser

import h800.arguscard


def main():
    parser = OptionParser("usage: %prog filename")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    filename = args[0]

    if not os.path.exists(filename):
        parser.error("Filename %s does not exist!" % filename)
        sys.exit(1)

    inlines = []
    with open(filename, 'r') as f:
        inlines = f.readlines()

    d = arguscard.Deck(inlines)

    logsection = d.log_section
    logsectioncol8 = d.log_section_col8

    for line in inlines:
        if logsection == None:
            if line.startswith("# Filename: "):
                infilename = line.split()[2].strip()
                if '.' in infilename:
                    infilename = infilename[:infilename.index('.')]
                logsection = infilename.replace('_', ' ')
                logsectioncol8 = '@'
        if line.startswith("# Pages: "):
            pageRange = line.split()[2].strip()
            if '-' in pageRange:
                start = int(pageRange.split('-')[0])
                end = int(pageRange.split('-')[1])
            else:
                start = end = int(pageRange)

    if logsection == None:
        parser.error("Cannot determine log section!")
        sys.exit(1)

    if start > end:
        parser.error("Invalid page numbers!")
        sys.exit(1)

    numdigits = len(str(end))

    outlines = []
    outlines.append("\n")
    outlines.append("L      %s%s\n" % (logsectioncol8, logsection))
    for pagenum in range(start, end+1):
        outlines.append("\n")
        outlines.append("# Page %d\n" % pagenum)
        outlines.append("#      %s%-72s USER'S OWN PAGE NO.%4s        PAGE%4s\n" % (logsectioncol8, logsection, pagenum-start+1, pagenum-start+1))
        outlines.append("\n")

    with open(filename, 'a') as f:
        f.writelines(outlines)


if __name__ == "__main__":
    main()
