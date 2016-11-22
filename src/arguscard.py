#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# ARGUS Punch-Card Classes
# ========================
#
# ARGUS-format punch-card support for the H800.

from __future__ import print_function
import sys

import punchcard


_WIDTH = 120
_FIELDS = [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]
_FIELDNAMES = ["column1", "lognum", "column8", "label", "operation", "operand1", "operand2", "operand3", "misc", "remarks"]


class Card(punchcard.PunchCard):
    """A simple class to represent an ARGUS punch card."""
    def __init__(self, line, width=_WIDTH, fields=_FIELDS, fieldnames=_FIELDNAMES, filename=None, linenum=0):
        super(Card, self).__init__(line, width=width, fields=fields, fieldnames=fieldnames, filename=filename, linenum=linenum)
        if self.column1 == 'P' or self.column1 == 'R':
            self._record["label"] = None
            self._record["operation"] = None
            self._record["operand1"] = None
            self._record["operand2"] = None
            self._record["operand3"] = None
            self._record["misc"] = None
            self._record["remarks"] = self._line[9:].strip()
        if self.column1 == 'L':
            self._record["remarks"] = self._line[9:].strip()

    @property
    def column1(self):
        return self._record["column1"]

    @property
    def lognum(self):
        return self._record["lognum"]

    @property
    def column8(self):
        return self._record["column8"]

    @property
    def label(self):
        return self._record["label"]

    @property
    def location(self):
        return self._record["label"]

    @property
    def operation(self):
        return self._record["operation"]

    @property
    def operand1(self):
        return self._record["operand1"]

    @property
    def addressa(self):
        return self._record["operand1"]

    @property
    def operand2(self):
        return self._record["operand2"]

    @property
    def addressb(self):
        return self._record["operand2"]

    @property
    def operand3(self):
        return self._record["operand3"]

    @property
    def addressc(self):
        return self._record["operand3"]

    @property
    def sequence(self):
        return self._record["misc"]

    @property
    def remarks(self):
        return self._record["remarks"]


class Deck(punchcard.Deck):
    """A simple class to represent a deck of ARGUS punch-cards."""
    def __init__(self, lines=None, file=None, width=_WIDTH, fields=_FIELDS, cardclass=Card):
        super(Deck, self).__init__(lines=lines, file=file, width=width, fields=fields, cardclass=cardclass)
        self._logSection = None
        self._logSectionCol8 = None
        for card in self._cards:
            if card.record["column1"] == 'L':
                # This will only recognise the first log section in a deck.
                self._logSection = card.line[8:81].strip()
                self._logSectionCol8 = card.record["column8"]
                break

    @property
    def log_section(self):
        return self._logSection

    @property
    def log_section_col8(self):
        return self._logSectionCol8


def main():
    # Simple tester.
    lines = """
L      @XYZ TESTING 123

 0020   L BACKUP   SPEC                                       BACKUP
 0021   L PRINT PS SPEC                                       PRINT PS

 0030   A999999    ALF          09999990
 0031   ASTRISK    ALF          *
 0032   COMA 1962  ALF          , 1962
 0033   DASH 1T3   ALF          ---

 0035   PASSS RE   ALF          RE: ASSE
 0036   MANUS RE   ALF            RE: MA
 0038   PASS S EQU ALF            = ASSE
 0039   MANU S EQU ALF              = MA
 0046   Y COLYUM 1 ALF          Y      3
 0047   PMAX9 MSJ  ALF          PMAX = 9
 0048   S BLANKS   ALF

 0049   S BLOTS    ALF          ████████
 0050   S COLON C1 ALF          :
 00505  S SIGH     ALF          (SIGH)

 0055   W 254P     ALF          254+

# Page 110
#      @YUL SYSTEM PASS 0 SERVICE MODULE                                         USER'S OWN PAGE NO.   3        PAGE  70

P0068   ONE-WORD ALPHABETIC CONSTANTS CONCLUDED.

 0069   W NONE     ALF           (NONE)
 0070   W OBS      ALF            *OBS*
 0071   W OBSOLET  ALF          OBSOLETE
 0085   ZSUP ONE   ALF                 1


R0086   ALPHABETIC ARRAYS.

 0088   BKUP LINE  ALF,4         DIRECTORY LISTING OF YULPROGS #
 0089   BUREL MSG  ALF,2        BACKUP RELABELED
 0090   CHEDL MSG  ALF,3        CHECK DIRECTORY LISTING
 0091   COMPU MSG  ALF,2
 0092   COMUS MSG  ALF,3        COMPUTER IS STILL IN USE
 0093   CONCN MSG  ALF,5        CONFLICT WITH EXISTING COMPUTER NAME-
 0094   DCLAV MSG  ALF,3        DECLARED AVAILABLE
 0095   DCLOB MSG  ALF,3        DECLARED OBSOLETE
 0096   DCLOK MSG  ALF,3        DECLARED CHECKED OUT
 0097   MANUS MSG  ALF,2        NUFACTURING FOR

# Page 111
#      @YUL SYSTEM PASS 0 SERVICE MODULE                                         USER'S OWN PAGE NO.   4        PAGE  71

P0098   ALPHABETIC ARRAYS CONTINUED.

 0099   MNTN LINE  ALF,4        YUL SYSTEM MAINTENANCE FUNCTION:
 0100   NEWCO MSG  ALF,3          NEW COMPUTER:
 0101   NEW LINE   OCT          0
 0102              ALF,5
 0103              ALF,5
 0104              ALF,5
 0105   NOMAT MSG  ALF,4        NO MATCH FOUND FOR THIS CARD:
 0106   NOTAV MSG  ALF,2        NOT AVAILABLE
 0107   NOW OP MSG ALF,4         NOW OPERATING FROM NEW YULPROGS

 0108   OBUWK MSG  ALF,4        FORMER BACKUP WILL BE WORKER
 0109   OP SLP MSJ ALF,2        OPERATOR ASLEEP
 0110   PASSS MSG  ALF,2        MBLY PASS █ FOR
 0111   PCH CARD   OCT          0
 0112              ALF,5
 0113              ALF,5
 0932   RUNOUT PR  TS           S 4SPACE      N,X2,1        GET LOG NO     C
 0933              SWS, D8T12   S ZERO                      N,AU2
 0934              MT           S BLANKS      15            N,X2,1
 0935              WD           Z,X2          OCTAL 20      Z,X2
 0936              S, PHI PRINT 2,0
 0937              S, PHI PRINT 2,0
 0938              S, PHI PRINT 2,0                                             FORCE LAST LINES THROUGH BUFPRINT.
 0940              S, MON TYPER W LIST DUN    SPRAMR +16    -                   ANNOUNCE END OF LISTING.

R0979   TO EACH.  WHEN THE LISTING IS FINISHED, GROUP B HOISTS A FLAG AND EXPIRES.


 0981   BACKUP     TS           S ZERO        COMMON        SET UP GPB     C    COMMUNICATION FLAG FOR END.
 0983              TS           Z,SC,4        N,SH          MON WAKE       C

 0984   BK1 VIA X0 TX           L BANK 1      -             Z,X0
 0985              TX           L DIRECTY     -             Z,X1
 0986              TX           PHI WAA       -             Z,X6
 0987              TS           YUL MASKS     Z,MXR         LIST LABL           START GROUP B GOING ON LISTING.

 0989              TX           1,1           -             YUL BU MSG +1
 0991              NA, CHAR8    1,0           S ONE         AMEND BUL           BRANCH IF ONLY MUST AMEND BACKUP LABEL.
""".splitlines()

    d = Deck(lines)
    import pprint
    pprint.pprint(d.records)
    assert d.log_section == "XYZ TESTING 123"
    assert d.log_section_col8 == "@"


if __name__ == '__main__':
    main()
