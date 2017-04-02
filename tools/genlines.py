#!/usr/bin/env python
#
# Python program to generate line numbers for ARGUS/MITIGUS format sources.
#
# Jim Lawton 2016-11-08
#
# ARGUS assembly language source cards are column-delimited lines in the form:
#
# 0        0         0         0         0         0         0         0         0         0         1         1         1
# 0        1         2         3         4         5         6         7         8         9         0         1         2
# 123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
#  NNNNNN S.....................................................................S R......................................R
#
# where NNNNNN is the card number (line number) and is max 6 decimal digits.
# The minimum field length is 4, zero-filled.
#
# S...S is the part of the line that contains source operations & operands.
# R...R is the part of the line containing remarks (comments). An 'R' in column
# 1 indicates a line comment.


import sys
from optparse import OptionParser


def main():
    parser = OptionParser("usage: %prog start end [step] [startcol] [endcol]")
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.error("Start and End numbers must be supplied!")
        sys.exit(1)

    leftzero = False
    if args[0].startswith('0') or args[1].startswith('0'):
        leftzero = True
    ndigits = len(args[0])
    if ndigits > 6:
        parser.error("Number of digits cannot be greater than 6!")
        sys.exit(1)
    ndigits = len(args[1])
    if ndigits > 6:
        parser.error("Number of digits cannot be greater than 6!")
        sys.exit(1)

    start = int(args[0])
    end = int(args[1])

    numdigits = len(str(end))
    if numdigits > 6:
        parser.error("Number of digits cannot be greater than 6!")
        sys.exit(1)

    minwidth = 4
    width = numdigits
    if width < minwidth:
        width = minwidth
    if width < ndigits:
        width = ndigits

    step = 1
    if len(args) >= 3:
        step = int(args[2])

    startcol = 2
    if len(args) >= 4:
        startcol = int(args[3])

    endcol = 7
    if len(args) >= 5:
        endcol = int(args[4])

    for i in range(start, end+step, step):
        print "%s%s%s" % ((startcol - 1) * ' ', "{num:{fill}{width}}".format(num=i, fill='0', width=width), (endcol + 2 - startcol - width) * ' ')


if __name__ == "__main__":
    main()
