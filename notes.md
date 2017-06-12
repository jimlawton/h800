
Honeywell H-x800 Notes
======================

Jim Lawton, February 2017. 

Notes accumulated from reading the H-1800 Programmers Reference Manual, and the YUL ARGUS sources. 


Endianess
---------

The Hx800 family of machines are a bit strange by modern standards. They are 48-bit memory machines with 16-bit or 32-bit register widths (depending on model/configuration). Memory data path is 48 bits wide. Register data path is 16 bits wide. Memory address space is word (48-bit) oriented rather than byte-oriented. Memory address range however is determined by register width. For the base H-800 machines (16-bit register width), the maximum addressable memory is 2^15, or 32768 48-bit words. For fully-configured H-1800 machines, the maximum addressable memory is 2^16, or 65536 48-bit words. This is achieved by adding an extra "array bit" to the special registers, and adding instructions (EBA, EBS) to manipulate the array bits.

The architecture is big-endian. Bit 1 is the MSB and bit N is the LSB. So, for example, memory words are 48 bits wide. They look like:

 01 02 03 ................... 46 47 48
 MSB                               LSB

However, there is no sub-48-bit access to memory, so the issue of endianess doesn't really apply.


Instruction Set
---------------

- BA    (Binary Add)
- BD    (Fixed Binary Divide)
- BM    (Binary Multiply)
- BS    (Binary Subtract)
- BT    (Binary Accumulate)
- CC    (Compute Orthocount)
- COREDUMP (?)
- CP    (Check Parity)
- CSCON (Cosequence Control)
- DA    (Decimal Add)
- DD    (Fixed Decimal Divide)
- DM    (Decimal Multiply)
- DOFF  (Demand Off)
- DON   (Demand On)
- DS    (Decimal Subtract)
- DT    (Decimal Accumulate)
- DUMP  (?)
- EBA   (Extended Binary Add)
- EBS   (Extended Binary Subtract)
- EX    (Extract)
- FBA   (Floating Binary Add)
- FBAE  (Floating Binary Add, Extended Precision)
- FBAU  (Floating Binary Add, Unnormalized)
- FBD   (Floating Binary Divide)
- FBM   (Floating Binary Multiply)
- FBS   (Floating Binary Subtract)
- FBSE  (Floating Binary Subtract, Extended Precision)
- FBSU  (Floating Binary Subtract, Unnormalized)
- FCON  (Conversion)
- FDA   (Floating Decimal Add)
- FDAU  (Floating Decimal Add, Unnormalized)
- FDD   (Floating Decimal Divide)
- FDM   (Floating Decimal Multiply)
- FDS   (Floating Decimal Subtract)
- FDSU  (Floating Decimal Subtract, Unnormalized)
- FFN   (Fixed-to-Floating Normalize)
- FLN   (Floating Less than, Normalized)
- FNN   (Floating Not Equal, Normalized)
- HA    (Half add)
- IT    (Item Transfer)
- LA    (Less than or equal, alphabetic)
- LN    (Less than or equal, numeric)
- MPC   (Multiprogram Control)
- MT    (Multiple Transfer)
- NA    (Not equal, alphabetic)
- NN    (Not equal, numeric)
- PR    (Proceed)
- PRA   (Print Alphabetic)
- PRD   (Print Decimal)
- PRO   (Print Octal)
- RB    (Read Backward)
- RF    (Read Forward)
- RT    (Record Transfer)
- RW    (Rewind)
- S     (Simulate)
- SCON  (Sequence Control)
- SIMULATE (?)
- SM    (Superimpose)
- SPCR  (Save Program Control Register) (?)
- SPE   (Shift Preserving Sign and Extract)
- SPS   (Shift Preserving Sign and Substitute)
- SS    (Substitute)
- SSL   (Shift and Select)
- STOP  (Stop calling program)
- SWE   (Shift Word and Extract)
- SWS   (Shift Word and Substitute)
- TN    (N-word Transfer)
- TS    (Transfer A to B, go to C)
- TX    (Transfer A to C)
- ULD   (Multiple Unload)
- WA    (Word Add)
- WD    (Word Difference)
- WF    (Write Forward)


Unknown ARGUS Opcodes
---------------------



Constants
---------

- Decimal
-- Signed constants assume high-order zeros. E.g. "+125": +00...0125, "-125": -00...0125. Decimals with all MSBs zero have to be negative.
--  Unsigned constants assume low-order zeros. E.g. "32": 3200...00.

- Hex
-- ARGUS hex numbers are specified as 0-9, B-G:
"0"-"9" : 0-9
"B": 10, 0x0A.
"C": 11, 0x0B.
"D": 12, 0x0C.
"E": 13, 0x0D.
"F": 14, 0x0E.
"G": 15, 0x0F.
Confusing or what...
-- To produce a binary number with zeros in the top 4 bits, it has to be something like "-G...".


SETLOC
------

Examples:
```
 0671              SETLOC TABLE
 0674              SETLOC TABLE -20000
 0004              SETLOC,1C    0             B1
 0675              SETLOC,4     0             B4
 083895            SETLOC,1
 3037              SETLOC,3C    1984          B1
 0003              SETLOC,1C    0             B1
 0353   (SETLOC)   EQUALS       B3T6
 172022            SETLOC,5     1024          B7
 172055            SETLOC,1
 280414            SETLOC       RL CD HLTH
 2811              SETLOC,7C    SIZ PASS 1    B1
 0001              SETLOC,6C    1024          B7
 00026             SETLOC,1C    0             B1
 2463              SETLOC,7C    SIZ PASS 2    B1                                PASS 1.5 IS OVERLAID BY PARTICULAR PAS2.
 3276              SETLOC,1     HEALTH
 0004              SETLOC,1C    0             B1
 016015            SETLOC,6C    512           B5
 016095            SETLOC,1
 016605            SETLOC,6
 02085             SETLOC,1
 1706              SETLOC,7C    SIZ PASS 3    B1
 0004              SETLOC,2     SIZ PASS 1    B1
 0004              SETLOC,2     SIZ PASS 2    B1
 0011              SETLOC,4     768           B5
 0022              SETLOC,3     0             B5
 0004              SETLOC,2     SIZ PASS 3    B1
 0003  *           SETLOC,2     SIZ PASS 1    B1
 01169             SETLOC,3     0             B5
 011692            SETLOC,4     15            B5
 0003              SETLOC,2     SIZ PASS 2    B1
 00582             SETLOC,4     768           B5
 01052             SETLOC,2
 0631              SETLOC,3     0             B5
 0004              SETLOC,2     SIZ PASS 3    B1
 0004              SETLOC,2     SIZ PASS 3    B1
 0004              SETLOC,2     SIZ PASS 1    B1
 01432             SETLOC,3     0             B5
 01434             SETLOC,4     9             B5
 00432             SETLOC,2     SIZ PASS 2    B1
 0060              SETLOC,4     768           B5
 0112              SETLOC,2
 1156              SETLOC,3     0             B5
 1405              SETLOC,5     512           B2
 0004              SETLOC,2     SIZ PASS 3    B1
 2924              SETLOC,5     1056          B7
 3301              SETLOC, 2    1152          B7
 0004  *           SETLOC,2     SIZ PASS 1    B1
 01362             SETLOC,3     0             B5
 01364             SETLOC,4     15            B5
 0004              SETLOC,2     SIZ PASS 2    B1
 0061              SETLOC,4     768           B5
 0116              SETLOC,2
 0705              SETLOC,3     0             B5
 0004              SETLOC,2     SIZ PASS 3    B1
 0004              SETLOC,2     SIZ PASS 1    B1
 01862             SETLOC,3     0             B5
 01864             SETLOC,4     9             B5
 0044              SETLOC,2     SIZ PASS 2    B1
 0062              SETLOC,4     768           B5
 0126              SETLOC,2
 1064              SETLOC,3     0             B5
 1246              SETLOC,5     512           B2
 0004              SETLOC,6C    SIZPASS1 +64  B1
 0004              SETLOC,1     0             B2
 0388   WHAT SUBD  SETLOC
 0004              SETLOC,1     0             B2
 0004              SETLOC,2     0             B4
 3002              SETLOC,5C    OVERSPIL      B4
 0004              SETLOC,1     0             B4
```

The following sets location counter to "upper half of bank 7":

    0001              SETLOC,6C    1024          B7

I think that means that the arguments have the following meanings:

    1:  6C      Bank 6, "Common"
    2:  1024    Offset from the start of the bank?
    3:  B7      Bank number, i.e. 7.

Taking another example:

    00026             SETLOC,1C    0             B1

gives:

    1:  1C      ?
    2:  0       Offset from the start of the bank, i.e. 0?
    3:  B1      Bank number, i.e. 1.

Q: Do bank numbers start at 0 or 1?


EQUALS
------

Examples:
```
 0109   PROG NAME  EQUALS       YUL PASS 0                                      (FOR INTERPASS STORAGE PURPOSES).
 0632   AMTF       EQUALS       384
 0637   DAMN ZERO  EQUALS       0
 0639   BIT 34     EQUALS       4 C6
 0645   1 C6       EQUALS       BIT 36
 0647   W REVISION EQUALS       DR UMA MSG +1
 0650   END THR    EQUALS       14342
 0656   BANK 1     EQUALS       L DIRECTY
 0657   ACO2       EQUALS       B10T12
 0658   AMPRSANS   EQUALS       DEC ALF M3
 0663   L STOPPER  EQUALS       CAC3
 0354   INRECNT    EQUALS       SUBSTRAB +5
 0355   LOC LOC    EQUALS       COMMON +7
 0356   (ERASE)    EQUALS       BIT 2
 0358   (2CTAL)    EQUALS       B2B6
 0359   TEN C1     EQUALS       (INSTR)
 280454 SIZ PASS 1 EQUALS       FILL - PROG NAME + 64
 280456 M OP THRS  EQUALS       FILL +64
 24289  SIZ PASS 2 EQUALS       PATCHES - PROG NAME + 10
 0852   L STOPPER  EQUALS       CAC3
 0322   S STOPPER  EQUALS       S CAC 3
```

TBD


MODLOC
------

Examples:
```
 2804   FILL       MODLOC       64
 1691   FILL       MODLOC       64
 0966   MASK LOC   MODLOC       64
 1128   MASK LOC   MODLOC       64
```

TBD


ASSIGN
------

Examples:
```
 0589   MONITOR    ASSIGN       7,0
 0590   PHI TAPE   ASSIGN       7,1
 0591   PHI SNACH  ASSIGN       7,2
 0592   PHI PEEK   ASSIGN       7,3
 0593   EOR        ASSIGN       7,4
 0594   PHI LOAD   ASSIGN       7,7
 0595   PHI READ   ASSIGN       7,15
 0596   MON RLEAS  ASSIGN       7,19
 0597   PHI PRINT  ASSIGN       7,23
 0598   MON EOFRI  ASSIGN       7,31
 0599   PHI DATE   ASSIGN       7,36
 0600   PHI SENTR  ASSIGN       7,40
 0601   PHI A2D    ASSIGN       7,41
 0602   PHI ABORT  ASSIGN       7,46
 0603   BASE ADDR  ASSIGN       7,47
 0604   MON UNLOK  ASSIGN       7,85
 0605   MON SGSNA  ASSIGN       7,91
 0606   MON WAKE   ASSIGN       7,99
 0607   MON REL GP ASSIGN       7,100
 06072  MON RELOX  ASSIGN       7,103
 0608   MON SN QIP ASSIGN       7,111
 0609   DISCAP     ASSIGN       7,114
 0610   MON SLEEP  ASSIGN       7,166
 0611   MON PRADS  ASSIGN       7,174
 0612   MON LCARD  ASSIGN       7,178
 0613   MON RELCD  ASSIGN       7,180
 0614   MON PUNCH  ASSIGN       7,191
 0615   PHI LABEL  ASSIGN       7,195
 0616   DISC STAT  ASSIGN       7,210
 0617   MON SNCOR  ASSIGN       7,212
 0618   MON TYPER  ASSIGN       7,215
 0619   MON PCR    ASSIGN       7,220
 0620   DISC CHEK  ASSIGN       7,221
 0621   MON TADDR  ASSIGN       7,223
 0622   GET LOG NO ASSIGN       7,225
 06229  DISC READ  ASSIGN       7,239
 0623   1800 AB SW ASSIGN       7,241
 0624   DISC WRIT  ASSIGN       7,247
 0625   PACK DATE  ASSIGN       6,100
 0626   YUL DATE   ASSIGN       6,101
 0627   YUL LOG    ASSIGN       6,104
 0628   YUL LOG A  ASSIGN       6,105
 0629   $PAR IDLE  ASSIGN       6,106
 083695 L COPBS BJ ASSIGN       0,39
 0837   NO CORE    ASSIGN       0,72
 08371  DO BKUP BJ ASSIGN       0,86
 08372  YUL DA LZS ASSIGN       0,119
 08373  B SERVICE  ASSIGN       0,138
 08374  ACA OTHE B ASSIGN       0,141
 0155   HEALTH     ASSIGN       0,0
 0156   CARDNO WD  ASSIGN       0,1
 0157   LOC FIELD  ASSIGN       0,2
 0158   OP FIELD   ASSIGN       0,3
 0159   ADDRESS 1  ASSIGN       0,4
 0160   ADDRESS 2  ASSIGN       0,5
 0161   DATE WORD  ASSIGN       0,9
 0214   LINE       ASSIGN       0,0
 02145  CUSS LIST  ASSIGN       1,0
 022201 BIT 1      ASSIGN       1,064
 022202 BIT 2      ASSIGN       1,065
 022203 BIT 3      ASSIGN       1,066
 0264   ALL DONE   ASSIGN       N,R3
 0265   FOUND SYM  ASSIGN       N,R4
 0266   OLD SPACE  ASSIGN       N,X5
 08496  YUL DATE   ASSIGN       6,101
 0850   YUL LOG    ASSIGN       6,104
```

TBD


RESERVE
-------

Examples:
```
 0360   TRONDEX    RESERVE      15
 0361   AUTH NAME  RESERVE      2
 0363   TYP RTURN  RESERVE      1
 0364   SORS LINE  RESERVE      16
 0703              RESERVE      1
 07372  PHI ARG BJ RESERVE      1
 1000   TYPER MXR  RESERVE      1
 2166              RESERVE      1
 2824   LEADR MSG  RESERVE      8
 00022  CUSS LIST  RESERVE      64
 0322   REQ LIST   RESERVE      117
 1923   COPY AREA  RESERVE      262
 0316   WIRE NO    RESERVE      1
 0317   REQ LIST   RESERVE      240
```

TBD


SPEC
----

- Special register, 16-bit word (see p29); note: systems with greater that 32KW have 24-bit special registers)

Examples:
```
 09272             SPEC                                     END RD4
 1072   END SY BUF SPEC                                     4759
 1073              SPEC                                     5759
 1076   WS3 SY SPX SPEC                                     EN TAP SYM
 1077              SPEC                                     TAPE SYM
 10771  L ZERO     SPEC                                     ZERO
 1078   L ONES     SPEC                                     ONES
 1079   SJ LIM     SPEC                                     13023
 1080   WS3 SST P8 SPEC                                     WS3 SST +8
 1081   L B BUF8   SPEC                                     13023
 0124   SYM PLACE  SPEC,B8                                  DAMN ZERO      -
 0126   L COP BUFS SPEC,B7                                  768
 0567   L AV TABLE SPEC,B4                                  DAMN ZERO
 0570   GB SWITCH  SPEC,G0                                  N,R2
 0571   BANK 3     SPEC, BB                                 DAMN ZERO
 0573   END BANK B SPEC, BB                                 2039
 0576   L ONES     SPEC,B7                                  7
 0577   BUF NAMES  SPEC,B5                                  928
 0586   SPEC ONE   SPEC,B0                                  1
 2514   MON WAA    SPEC,B7                                  600
 3230              SPEC,B7                                  1159
 3231              SPEC,B7                                  1155
 0240   L SYM TAB  SPEC,B8                                  DAMN ZERO      -
 0296   XFR LIMIT  SPEC,BC                                  2043
 0297              SPEC,BC                                  2046
 0298              SPEC,BG                                  2044
 01178  PHI WAA    SPEC,B7                                  600
```


CAC
---
- "Complete Address Constant"
-- This is for forming compressed address constants. Since H-x800 words are 48 bits wide, and addresses are only 16 bits, then 3 addresses can be packed into one memory word. This is what CAC does. It seems to take from one to three arguments, I assume any unspecified argument is replaced by zero in the memory word formed, but that is a guess.

Examples:
```
 0292   INIT WD 8  CAC,B7       6             6             10
 0258   L DIRECTY  CAC           2048                       14336               ADDRESSES OF B1, B7 (0,83).
 0288   L PGHED P3 CAC          30720                       PAGE HEAD +3        DEPAGINATOR & HEADLINE ADDRESS (0,101).
 0561   RLS CO PCH CAC                        NUMERALS      16
 0574   I SYM THRS CAC          8192                        8192
 0314   SOURCE     CAC          15043         TAPE CARD -1  REAL CARD -1
 0322   L PRSV CNS CAC          INSRT LUP                   PRESERVE
 0336   L BOTH CDS CAC          24576         TAPE CARD +1  REAL CARD +1        ALSO Y COLUMN 1.
 172021 L TAP CARD CAC          EXPANDER      TAPE CARD +5  TAPE CARD
 1971              CAC                        NO MODIF      FOUND RNB           SET UP TO LOOK FOR SIGNS INITIALLY.
 0243   L CD TYPES CAC          1024                        CARD TYPS
 0244   CARD TYPS  CAC          MODIFY        14            END OF
 0245              CAC          CARD NO       14            END ERROR
 0250              CAC          OCTAL         DAMN ZERO     DECIMAL
 02561             CAC                        3             SEGNUM
 0430   L FINI 1P  CAC          CARD +3                     C,+1
 0466   L FINI 1P  CAC                                      C,+1
 0252   E BUFFERS  CAC          30720         4500          5500
 00251  A4 ELEFT P CAC          6149                        GOT ELEFP
 00252 *A4 FLEFT P CAC          6165          1024          A4 FLEFTO      -
 00505             CAC                        6149                         -
 00508             CAC                        6581          1024           -
 0122              CAC          CODES 41                    BAD CODE
 0148   IMPLADS    CAC          1                           0              -
 0149              CAC          14                          2              -
 0150              CAC          21                          15             -
 0151              CAC                                      3071           -
 00292 *B2 FLEFT P CAC          6165          2048          B2 FLEFTO      -
 00765             CAC                        8229
 00774             CAC                        6149                         -
 00777             CAC                        7061          2048           -
 1680   L INT OPPP CAC                                      INT OP POP
 0024   SC TYP TAB CAC          COUNT STA     1024          SACO MEMO      -
 00262 *SC FLEFT P CAC          6165          1024          SC FLEFTO      -
 00545             CAC                        6149                         -
 00548             CAC                        6245          1024           -
 0160   IMPLADS    CAC          1                           0              -
 0161              CAC          14                          2              -
 0162              CAC          21                          15             -
 0163              CAC                                      3071           -
 0033  *AG FLEFT P CAC          6165          2048          AG FLEFTO      -
 12786  M AV TABLE CAC          11032         11140         8192
```


MASKGRP
-------

What does MASKGRP do?

Examples:

    0005              MASKGRP,1    S,0           F,0
    0004  *           MASKGRP,3    S,1           F,1
    0005  *           MASKGRP,1    S,1           F,1
    018415            MASKGRP      S,0           F,0
    0002              MASKGRP,6    S,0           F,0

```
 0005              MASKGRP,1    S,0           F,0
 0002              MASKGRP,6    S,0           F,0
 2465              MASKGRP,7    S,7           F,7
 32032             MASKGRP      S,0           F,0
 0005              MASKGRP,4    S,1           F,1
 0004  *           MASKGRP,3    S,1           F,1
 048705            MASKGRP      S,1           F,1
 0005  *           MASKGRP,1    S,1           F,1
```

MASKBASE
--------

TBD

Examples:
```
 0246   YUL MASKS  MASKBASE     S,0           F,0                               (0,77).
 006132 P1 MASKS   MASKBASE     S,0           F,0                               CAC2 HOLDS L NEXT SUB.
 006132 GENL MXR   MASKBASE     S,0           F,0
 2511   P1▪5 MXR   MASKBASE     S,7           F,7
 0237   P3 MASKS   MASKBASE     S,0           F,0
 0009   1800 MXR   MASKBASE     S,1           F,1
 0057   AGC4 MXR   MASKBASE     S,1           F,1
 0072   BLK2 MXR   MASKBASE     S,1           F,1
 1693   I GENL MXR MASKBASE     S,0           F,0
 0049   SACO MXR   MASKBASE     S,1           F,1
 0088   AGC MXR    MASKBASE     S,1           F,1
 12789  I GENL MXR MASKBASE     S,0           F,0
 0306   AGC4 MSKS  MASKBASE     S,1           F,1
 0302   BLK2 MSKS  MASKBASE     S,1           F,1
 0159   SACO MSKS  MASKBASE     S,1           F,1
```


STOP
----

- MPC variant; see p113.

Examples:
```
```


SIMULATION
----------
 - Is there any free space in the instruction space to add special instructions for simulation use? 
 - Dedicate a special memory address as a write-only buffer for debug output.
 - Some kind of assert would be very useful in order to write code to test the instruction set of the simulator.

