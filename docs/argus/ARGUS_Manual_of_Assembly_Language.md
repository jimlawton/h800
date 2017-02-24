# ARGUS 
## AUTOMATIC ROUTINE GENERATING AND UPDATING SYSTEM
### MANUAL OF ASSEMBLY LANGUAGE

Honeywell Electronic Data Processing

Price . . . . . $3.50

Questions and comments regarding this manual should be addressed to:

    Honeywell Electronic Data Processing
    Merchandising Division
    60 Walnut Street
    Wellesley Hills 81, Massachusetts

## TABLE OF CONTENTS

```
                                                                           Page
  Section I     Introduction ..............................................   1
                    The ARGUS System ......................................   1
                    The Assembly Program ..................................   4
                        Symbolic and Relative Reference ...................   4
                        Allocation ........................................   4
                        Translation .......................................   4
                        Library Routine Insertion .........................   4
                        Sort Generation ...................................   4
                        Relocation ........................................   5

  Section II    The Honeywell 800 System ..................................   7
                    Word Structure ........................................   7
                    Information Storage ...................................   7
                    Sequence Control ......................................   8
                    Command Codes .........................................   9
                    Addresses .............................................   9
                    Masks .................................................  10

  Section III   The ARGUS Coding Form .....................................  13
                    Location Field (Columns 1-10) .........................  13
                    Command Code (Columns 11-23) ..........................  13
                    Address Fields (Columns 24-37, Columns 38-51, 
                        Columns 52-65) ....................................  15
                    Line Number (Columns 66-73) ...........................  15
                    Identification (Columns 74-80) ........................  16
                    Remarks (Columns 66-80) ...............................  16

  Section IV    Tags  .....................................................  17
                    Symbolic Tags .........................................  17
                    Special Register Tags .................................  18
                    Mask Tags .............................................  19
                    Link Tags .............................................  19
                    Out-of-Sequence Words .................................  20
                    Definition of Tags ....................................  20

  Section V     Addresses .................................................  21
                    Direct Memory Location Address ........................  21
                        Address Arithmetic ................................  23
                    Direct Special Register Address .......................  24
                    Indexed Memory Location Address .......................  24
                    Indexed Special Register Address ......................  25
                    Indirect Memory Location Address ......................  26
                    Indexed Indirect Memory Location Address ..............  27
                    Inactive Address ......................................  28
                    Stopper Address .......................................  28
                    Numbers in Address Fields .............................  28

  Section VI    Program Structure .........................................  29
                    Segmentation ..........................................  29
                    Segment Loading .......................................  30
                    Subsegmentation .......................................  31
                    Allocation ............................................  32
                    Relocation ............................................  33

  Section VII   Machine Instructions ......................................  37
                    General Instructions ..................................  37
                        Sequence Change Instructions ......................  38
                        Field Instructions ................................  38
                        N-word Instructions ...............................  41
                    Peripheral Instructions ...............................  42
                    Shift Instructions ....................................  44
                    Scientific Instructions ...............................  46
                    Simulator Instructions ................................  47
                    Multiprogram Control ..................................  49
                    Extended Instructions .................................  50
                        Program Control Instructions ......................  50
                        Print Instructions ................................  61

  Section VIII  Assembly Control Instructions .............................  53
                    SETLOC ................................................  53
                    EVEN ..................................................  55
                    SIMULATE ..............................................  55
                    MODLOC ................................................  56
                    ASSIGN ................................................  56
                    TAS (Temporary Assignment) ............................  57
                    EQUALS ................................................  57
                    RESERVE ...............................................  58
                    MASKGRP ...............................................  59
                    END ...................................................  61
                    The RES Table .........................................  61

  Section IX    Constants .................................................  63
                    Data Constants ........................................  63
                        ALF (Alphanumeric Constant) .......................  63
                        OCT (Octal Constant) ..............................  64
                        DEC (Fixed Decimal Constant) ......................  64
                        FXBIN (Decimal to Fixed Binary Translation) .......  65
                        FLDEC (Floating-Point Decimal Constant) ...........  65
                        FLBIN (Floating-Point Binary Constant) ............  66
                        EBC (Extended Binary Constant) ....................  66
                    Control Constants .....................................  67
                        SPEC (Special Address Constant) ...................  67
                        CAC (Complete Address Constant) ...................  69
                        MASKBASE (Mask Base Address Constant) .............  69
                        CONTROL (Program Control Constant) ................  71
                        M (Mixed Constant) ................................  72
                        TAC (Tape Address Constant) .......................  73
                        LINK (Linkage Constant) ...........................  73
                        SEGNAME (Segment Name Constant) ...................  73
                        SUBCALL (Subroutine Call Constant) ................  74

  Section X     Masking ...................................................  75
                    Designated Masks ......................................  75
                    Generated Masks .......................................  76
                    Mask Groups ...........................................  76
                    Referencing Masks .....................................  77
                    Subroutine and Macrocoding Masks ......................  79
                    Mask Pools ............................................  79

  Section XI    ARGUS Updating Function ...................................  81
                    ARGUS .................................................  81
                    Program Directors .....................................  81
                        U,ELIMPROG ........................................  82
                        U,REASSEMB ........................................  82
                        U,CORRECT .........................................  82
                        U,NEWVERS .........................................  84
                        U,NEWPROG .........................................  84
                    Programmer Macro Routine Markers ......................  84
                        MACRODEF ..........................................  84
                        FINIS .............................................  85
                    Segment Directors .....................................  85
                        ELIMSEG ...........................................  85
                        SEGMENT ...........................................  85
                        PROGRAM ...........................................  86
                    Test Data Directors ...................................  87
                        TESTDATA ..........................................  87
                        ELIMDATA ..........................................  87
                    Test Data Detail Cards ................................  87
                    Debugging (Derail) Pseudo Instructions ................  88
                        ELIMDERL ..........................................  88
                    Main Coding ...........................................  88
                        DELETE ............................................  89
                    ENDARGUS ..............................................  89
                    Ordering the ARGUS Input Deck .........................  89
                    Equipment Requirements for the Updating Run ...........  91

  Section XII   Output from ARGUS Assembly Operation ......................  93
                    ARGUS Listing .........................................  93
                    Analyzer ..............................................  94
                    Programming Errors Detected ........................... 102
                    Input Errors Detected ................................. 102

  Section XIII  Library Routines .......................................... 105
                    Macro Routines ........................................ 105
                    Programmer-Defined Macro Routines ..................... 107
                    Subroutines ........................................... 107

  Appendix A.   Writing Library Routines and the Use of LAMP .............. 109
                    Writing Macro Routines ................................ 109
                    Writing Subroutines ................................... 112
                    Type 1 Calling Sequence ............................... 118
                    Type 2 Calling Sequence ............................... 120
                    Special Calling Sequences ............................. 123
                    LAMP (Library Additions and Maintenance Program) ...... 126
                        LAMP .............................................. 126
                        ENDLAMP ........................................... 126
                    Macro Routine Processing .............................. 126
                        MACRODEF .......................................... 126
                        FINIS ............................................. 127
                        ELIMMAC ........................................... 127
                    Subroutine Processing ................................. 127
                        NEWSUB ............................................ 127
                        ELIMSUB ........................................... 128
                    Output from LAMP ...................................... 128

  Appendix B.   Symbolic Program Tape Layout .............................. 131
                    Tape Label Record ..................................... 131
                    Loader ................................................ 131
                    Systems Program File .................................. 131
                    Symbolic Program File ................................. 132

  Appendix C.   Assembly Equipment Configuration Code ..................... 135

  Appendix D.   Tape, File, and Record Identification ..................... 137
                    Tape Label Record ..................................... 137
                    File and Program Identification Records ............... 138
                    Segment Identification Records ........................ 139
                    End-of-Information Records ............................ 139
                    Banner Words .......................................... 139
                    Summary ............................................... 140

  Appendix E.   Honeywell 800 Machine Instructions ........................ 141
                    General Instructions .................................. 141
                    Shift Instructions .................................... 143
                    Simulator Instructions ................................ 144
                    Peripheral Instructions ............................... 144
                    Extended Instructions ................................. 145
                    Scientific Instructions ............................... 146
```

## LIST OF ILLUSTRATIONS

```
Figure      1.  Honeywell 800 Automatic Programming System ................   2
Figure      2.  Honeywell 800 Word Forms ..................................   8
Figure      3.  The ARGUS Coding Form .....................................  14
Figure      4.  The ARGUS Input Card ......................................  15
Figure      5.  Special Register Names, Subaddresses, and 
                    Mnemonic Addresses ....................................  19
Figure      6.  Summary of Addresses ......................................  22
Figure      7.  Example of Program Relocation .............................  35
Figure      8.  ARGUS Mnemonic Operation Codes for Honeywell 800 Machine
                    Instructions ..........................................  39
Figure      9.  Designation and Referencing of Masks ......................  78
Figure     10.  ARGUS Listing - General Format ............................  95
Figure     11.  ARGUS Listing - Data Constants ............................  96
Figure     12.  ARGUS Listing - Equals and Reserve Instructions and 
                    Remarks Cards .........................................  97
Figure     13.  ARGUS Listing - Analyzer Lines ............................  98
Figure     14.  Sample ARGUS Listing (With Analyzer) ......................  99
Figure     15.  Programming Errors Detected During Assembly ............... 100
Figure    A-1.  Sample Macro Routine in Generalized Form .................. 113
Figure    A-2.  Specification Sheet for Macro Routine SRCHEQU ............. 114
Figure    A-3.  Macro Instruction for Sample Routine and Resulting 
                    Specialized Coding .................................... 116
Figure    A-4.  Type 1 Calling Sequence ................................... 118
Figure    A-5.  Type 2 Calling Sequence ................................... 120
Figure    A-6.  Special Calling Sequence CALLMAC .......................... 124
Figure    A-7.  Special Calling Sequence DBLSUM ........................... 125
Figure    B-1.  Over-all Layout of the Symbolic Program Tape .............. 133
```

## NOTE

This is the fifth printing of _The ARGUS Manual of Assembly Language_, edition `DSI-23C`.  The following differences are noted between this and the previous printing.

1.  The maximum size of main memory is 32,768 words (page 7).  Therefore, a bank indicator may range from `0` to `G` (hexadecimal) and the number of memory modules in an equipment configuration code (page 135) may range from 1 to 8.
2.  If no `SETLOC` precedes the first line of main coding in a segment, the Assembly Program assumes the existence of a defining `SETLOC` for subsegment 1, and the first line of main coding is allocated to bank `0`, location `0512` (page 54).
3.  Any mask groups which are stored in a common subsegment are assumed by the Assembly Program to be of maximum size.  Mask groups can be stored in a subsegment previously defined as common but not in a subsegment which is later defined as common (page 59).
4.  In [Section XII](#section-xii-output-from-argus-assembly-operation), information has been added on the printed directory of the SPT, the input errors detected by Assembly, and the provision for obtaining octal program listings.

## SECTION I: INTRODUCTION

### The ARGUS System

ARGUS, the Automatic Routine Generating and Updating System, is the core of the integrated automatic programming system for the Honeywell 800.  ARGUS is designed to minimize programmer effort and to maximize the efficiency of every phase of program preparation, form the initial coding through the checkout phase to actual production.  Wherever possible, the burden of routine, clerical operations is lifted from the programmer and the full power of the Honeywell 800 is brought to bear on such operations.  The file-of-programs approach, whereby batches of programs are assembled, tested, modified, and scheduled for production, minimizes setup time by eliminating a great multiplicity of brief, repetitive computer runs.  The dynamic dumping technique employed by the Program Test System enables batches of programs to be tested at full machine speed and without interruption.  Diagnostic information is obtained without manual intervention, even if a programming error forces premature termination of a particular program under test.  In short, ARGUS achieves a mating between the efficiency of program preparation and the remarkable efficiency of production made possible by Honeywell parallel processing.

As illustrated in [Figure 1], ARGUS is composed of the following principal elements:
1. An Assembly Program which translates symbolic coding and produces operating programs in machine language (binary) on magnetic tape;
2. A Library of Routines containing both subroutines and macro routines, each thoroughly tested and capable of being incorporated into any program during assembly by the inclusion of a single pseudo instruction;
3. A Library Additions and Maintenance Program (LAMP) for adding and deleting routines and modifying existing routines in the library;
4. A Program Test System which operates a file of _unchecked_ programs at full machine speed, automatically obtaining requested information at points specified by the programmer for later analysis of program operation;
5. An Executive System which schedules checked-out programs for parallel processing, based on their individual hardware requirements, timing, and urgency, and then automatically loads and executes the scheduled programs.

A program to be processed on the Honeywell 800 may be prepared in ARGUS assembly language, as described in this manual, or it may be written in the language of either the Automath or FACT (Business) Compiler and automatically converted to assembly language.  In either case, the Assembly Program translates this language and produces an operating program in both symbolic and machine language in the symbolic program tape, which contains a file of programs being checked out, together with test data for each program.  This is accomplished as part of an updating run in which programs are added to or deleted from the symbolic program tape, and existing programs and test data are modified on the basis of information derived from the preceding checkout run.

### The Assembly Program

#### Symbolic and Relative Reference

#### Allocation

#### Translation

#### Library Routine Insertion

#### Sort Generation

#### Relocation

## Section II: The Honeywell 800 System

### Word Structure

### Information Storage

### Sequence Control

### Command Codes

### Addresses

### Masks

## Section III: The ARGUS Coding Form

### Location Field (Columns 1-10)

### Command Code (Columns 11-23)

### Address Fields (Columns 24-37, Columns 38-51, Columns 52-65)

### Line Number (Columns 66-73)

### Identification (Columns 74-80)

### Remarks (Columns 66-80)

## Section IV: Tags

### Symbolic Tags

### Special Register Tags

### Mask Tags

### Link Tags

### Out-of-Sequence Words

### Definition of Tags

## Section V: Addresses

### Direct Memory Location Address

#### Address Arithmetic

### Direct Special Register Address

### Indexed Memory Location Address

### Indexed Special Register Address

### Indirect Memory Location Address

### Indexed Indirect Memory Location Address

### Inactive Address

### Stopper Address

### Numbers in Address Fields

## Section VI: Program Structure

### Segmentation

### Segment Loading

### Subsegmentation

### Allocation

### Relocation

## Section VII: Machine Instructions

### General Instructions

#### Sequence Change Instructions

#### Field Instructions

#### N-word Instructions

### Peripheral Instructions

### Shift Instructions

### Scientific Instructions

### Simulator Instructions

### Multiprogram Control

### Extended Instructions

#### Program Control Instructions

#### Print Instructions

## Section VIII: Assembly Control Instructions

### SETLOC

### EVEN

### SIMULATE

### MODLOC

### ASSIGN

### TAS (Temporary Assignment)

### EQUALS

### RESERVE

### MASKGRP

### END

### The RES Table

## Section IX: Constants

### Data Constants

#### ALF (Alphanumeric Constant)

#### OCT (Octal Constant)

#### DEC (Fixed Decimal Constant)

#### FXBIN (Decimal to Fixed Binary Translation)

#### FLDEC (Floating-Point Decimal Constant)

#### FLBIN (Floating-Point Binary Constant)

#### EBC (Extended Binary Constant)

### Control Constants

#### SPEC (Special Address Constant)

#### CAC (Complete Address Constant)

#### MASKBASE (Mask Base Address Constant)

#### CONTROL (Program Control Constant)

#### M (Mixed Constant)

#### TAC (Tape Address Constant)

#### LINK (Linkage Constant)

#### SEGNAME (Segment Name Constant)

#### SUBCALL (Subroutine Call Constant)

## Section X: Masking

### Designated Masks

### Generated Masks

### Mask Groups

### Referencing Masks

### Subroutine and Macrocoding Masks

### Mask Pools

## Section XI: ARGUS Updating Function

### ARGUS

### Program Directors

#### U,ELIMPROG

#### U,REASSEMB

#### U,CORRECT

#### U,NEWVERS

#### U,NEWPROG

### Programmer Macro Routine Markers

#### MACRODEF

#### FINIS

### Segment Directors

#### ELIMSEG

#### SEGMENT

#### PROGRAM

### Test Data Directors

#### TESTDATA

#### ELIMDATA

### Test Data Detail Cards

### Debugging (Derail) Pseudo Instructions

#### ELIMDERL

### Main Coding

#### DELETE

### ENDARGUS

### Ordering the ARGUS Input Deck

### Equipment Requirements for the Updating Run

## Section XII: Output from ARGUS Assembly Operation

### ARGUS Listing

### Analyzer

### Programming Errors Detected

### Input Errors Detected

## Section XIII: Library Routines

### Macro Routines

### Programmer-Defined Macro Routines

### Subroutines

## Appendix A: Writing Library Routines and the Use of LAMP

### Writing Macro Routines

### Writing Subroutines

### Type 1 Calling Sequence

### Type 2 Calling Sequence

### Special Calling Sequences

### LAMP (Library Additions and Maintenance Program)

#### LAMP

#### ENDLAMP

### Macro Routine Processing

#### MACRODEF

#### FINIS

#### ELIMMAC

### Subroutine Processing

#### NEWSUB

#### ELIMSUB

### Output from LAMP

## Appendix B: Symbolic Program Tape Layout

### Tape Label Record

### Loader

### Systems Program File

### Symbolic Program File

## Appendix C: Assembly Equipment Configuration Code

## Appendix D: Tape, File, and Record Identification

### Tape Label Record

### File and Program Identification Records

### Segment Identification Records

### End-of-Information Records

### Banner Words

### Summary

## Appendix E: Honeywell 800 Machine Instructions

### General Instructions

### Shift Instructions

### Simulator Instructions

### Peripheral Instructions

### Extended Instructions

### Scientific Instructions
