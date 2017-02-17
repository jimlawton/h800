
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

- SETLOC (syntax unspecified)
- MODLOC (function unknown)
- STOP (MPC variant; see p113)
- ASSIGN
- RESERVE
- SPEC
-- Special register, 16-bit word (see p29); note: systems with greater that 32KW have 24-bit special registers)
- CAC (function unknown)
-- I think this is for forming compressed address constants. Since H-x800 words are 48 bits wide, and addresses are only 16 bits, then 3 addresses can be packed into one memory word. I think this is what CAC does, and I hypothesise that it stands for "Condensed Address Constant". It seems to take from one to three arguments, I assume any unspecified argument is replaced by zero in the memory word formed, but that is a guess.
- EQUALS
- MASKGRP (function unknown - declaration of masks, fields?)
- MASKBASE 


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

The following sets location counter to "upper half of bank 7":

    0001              SETLOC,6C    1024          B7

I think that means that the arguments have the following meanings:

    1:  6C      ?
    2:  1024    Offset from the start of the bank?
    3:  B7      Bank number, i.e. 7.

Taking another example:

    00026             SETLOC,1C    0             B1

gives:

    1:  1C      ?
    2:  0       Offset from the start of the bank, i.e. 0?
    3:  B1      Bank number, i.e. 1.

Q: Do bank numbers start at 0 or 1?


MASKGRP
-------

What does MASKGRP do?

Examples:

    0005              MASKGRP,1    S,0           F,0
    0004  *           MASKGRP,3    S,1           F,1
    0005  *           MASKGRP,1    S,1           F,1
    018415            MASKGRP      S,0           F,0
    0002              MASKGRP,6    S,0           F,0

-end-
