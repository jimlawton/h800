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

![Figure 1](images/figure_1.png?raw=true)

The updating run is normally followed by a program selection run which can prepare a program test tape, containing programs and test data to be executed during a checkout run, or a master relocatable tape, containing checked-out programs to be scheduled by Executive for production operation, or both.  Input to this run includes the symbolic program tape, plus an active program list which specifies the programs to be transferred to either of the output tapes.  Those programs transferred to the program test tape are accompanied by test data and by derail instructions which specify the kinds and amounts of diagnostic information to be generated during checkout and the program points where this information is to be generated.  The program test tape is the input to the checkout run, during which the ARGUS Program Test System executes each program on the tape, using the accompanying test data and generating the requested information at the specified points.  The information generated is printed in a variety of formats designed for convenient analysis by the programmer, who uses this information to specify the changes in programs and test data which will be effected during the next updating run.

Programs transferred to the master relocatable tape are accompanied by relocation information which Executive uses to modify memory and peripheral equipment assignments in order to schedule production programs for automatic parallel processing.  The master relocatable tape is the input to the Executive scheduling run, together with a proposed schedule which specified the programs to be scheduled, the memory and equipment requirements of each, and any necessary production sequence among the various programs.  Based on this information, Executive schedules groups of programs to be processed in parallel, relocates the scheduled programs, and records them in operating form on the production run tape.

The Executive run supervisor is also stored on the production run tape, along with the scheduled programs.  This routine executes the schedule, automatically loading the production programs, turning them on and off, and communicating with the operator as necessary.  Manual intervention during the production run is minimized, but may be used to alter the schedule being performed or to handle any unexpected occurrences.

### The Assembly Program

As noted above, the Assembly program translates coding written with mnemonic and symbolic cods and produces operating programs in machine language.  Programs written in assembly language are independent of fixed memory locations and may be modified, corrected, or expanded in assembly language by the computer.  The ARGUS Assembly Program offers the following automatic programming features: symbolic and relative reference, allocation, translation, library routine insertion, sort generation, and relocation.

#### Symbolic and Relative Reference

Since programs are written without reference to fixed memory locations, program words may be referred to by means of symbolic tags.  However, it is not necessary to tag all of the words of a program.  Untagged words may be referred to relatively, using address arithmetic to specify the desired location either:
1. Relative to the location of a tagged word; or
2. Relative to the location of the word containing the reference.

#### Allocation

Program words are automatically allocated in the high-speed memory according to the sequence in which they are assembled.  The programmer may specify the location of the first word in any sequence, if he so desires.  Although the allocation of memory locations normally proceeds automatically, flexibility is enhanced by the provisions for programmer control of this process.

#### Translation

ARGUS instructions are written using mnemonic operation codes, symbolic or relative addresses, and decimal numbers.  The Assembly Program translates these into the binary language of the Honeywell 800.  Constants written in alphabetic, decimal, octal, or mixed form are translated into binary-coded alphanumeric, fixed-point or floating-point binary-coded decimal, or fixed-point or floating-point binary form.

#### Library Routine Insertion

A library of useful, thoroughly tested subroutines and macro routines is readily available to each Honeywell 800 installation, so that frequently used coding is preserved for easy insertion into new programs.  Each subroutine or macro routine in the library is represented by a pseudo instruction which specifies the desired routine plus all parameters required for its execution.  These pseudo instructions may be included in a program as easily as machine instructions.  When they are processed, ARGUS obtains the corresponding coding from the library and inserts it into the program.

#### Sort Generation

Included in the Library of Routines is a group of sort generators which can produce routines tailored to specific sorting applications.  The programmer includes in his program a pseudo instruction which specifies the type of sort desired and the equipment available for its execution.  The description of the format of the data to be sorted is included with the data itself.  ARGUS sort routines are composed of two phases: a presort phase which produces ordered strings of data and a merge sort phase which combines these ordered strings to form a single over-all sequence.  A new and unique method of merging is used which takes optimum advantage of any available number of magnetic tape units.

#### Relocation

ARGUS retains a record of the structure of each program word so that any assembled program may be automatically relocated to operate in another portion of the high-speed memory or to utilize other special registers, magnetic tape units, or input/output terminal units.  This feature of ARGUS greatly facilitates the use of the parallel processing ability of the Honeywell 800.

## Section II: The Honeywell 800 System

### Word Structure

Information is handled by the Honeywell 800 in fixed-length words comprising 54 binary digits, or bits.  Six of these bits are reserved for the automatic checking circuits and may be disregarded by the programmer.  The 48 information bits of each word may be grouped to form several basic types of words as shown in Figure 2.

In an instruction, the information bits are divided into four 12-bit groups which represent the command code and the `A`, `B`, and `C` addresses, respectively.  The address groups normally designate the locations of operands, but in certain instructions they contain other special information.  The command code group contains, in addition to the operation code, other special information which depends upon the type of instruction.  The complement of Honeywell 800 machine instructions is presented in [Appendix E](#appendix-e-honeywell-800-machine-instructions)).

In a fixed-point constant, the 48 information bits may represent eight alphanumeric characters, 11 signed or 12 unsigned decimal or hexadecimal digits, 15 signed or 16 unsigned octal digits, 44 signed or 48 unsigned binary digits, or any combination of characters, digits, and bits not exceeding 48 bits.  Up to four individually signed fixed-point constants, having an aggregate of not over 44 bits, may be stored in a single word.  A floating-point constant may consist of a seven-bit exponent and a 40-bit mantissa, with sign, or a seven-bit exponent and a 10-decimal-digit mantissa, with sign.  [Section IX](#section-ix-constants) describes the specification of data constants in assembly language.

### Information Storage

The Honeywell 800 main (or high-speed) memory is composed of banks, each capable of storing 2048 machine words.  These memory banks are available in pairs called modules, and a system normally includes from one to four such modules (4096, 8192, 12,288 or 16,384 words).  Further expansion to 24,576, 28,672, or 32,768 words is also available.  Every main memory location is designated by a unique address, consisting of a bank indicator from `0` to `C` (hexadecimal) and a subaddress from `0000` to `2047`.

In addition, the Honeywell 800 contains a special control memory which selects instructions and operand addresses.  The control memory is fixed in size and consists of eight identical groups of 32 special registers each.  A special register is designated by a unique address, consisting of a group indicator from `0` to `7` and a subaddress from `00` to `31`.  Each special register has the capacity to store a complete main memory address (sign, bank indicator, and subaddress).

![Figure 2](images/figure_2.png?raw=true)

### Sequence Control

The operational control of an individual program is delegated to a specific special register group.  Each group includes a pair of functionally identical sequencing counters, called the sequence counter (`SC`) and the cosequence counter (`CSC`).  Whenever one of these counters selects an instruction for execution, the contents of the counter are automatically incremented by 1.  Most machine instructions have the ability to designate one of these counters as the source of the next instruction.  Those instructions which do not include this facility are followed by an instruction selected by the same counter.  Instructions which result in a programmed change of sequence always alter the contents of the counter designated as the source of the next instruction.


Also included in each special register group is a pair of history registers, called the sequence history register (`SH`) and the cosequence history register (`CSH`).  Whenever the contents of a sequencing counter are altered, other than by normal incrementing or direct addressing, the corresponding history register stores the incremented contents of the counter which produced the sequence change.  Thus it is possible to depart from a programming sequence and execute several instructions under control of the alternate counter before returning to the original sequence, or to program a sequence change and automatically retain a record of the next step that would have been performed had the change not occurred.

### Command Codes

The command code group in a Honeywell 800 machine instruction contains an operation code which specifies the instruction to be performed.  Depending upon the type of instruction specified, this group may also contain such information as a peripheral code, a partial mask address, memory designator bits which relate each of the three address groups to either main or control memory, and a bisequence bit which indicates the source of the following instruction.

Machine instructions are of five types: general, shift, peripheral, simulator, and scientific, as distinguished by the various command code formats.  The details of these formats are described in [Section VII](#section-vii-machine-instructions).  General instructions include arithmetic operations, information transfers, decisions, and other familiar data processing functions.  Many of these instructions can manipulate variable-length fields by the use of masks.  These are called field instructions.  Shift instructions are always performed with masked operands.  Peripheral instructions perform all operations which involve magnetic tape units and terminal input/output equipment, such as reading, writing, and rewinding.  Simulator instructions are defined by the programmer to represent, by means of a single instruction, an entire body of coding.  Scientific instructions manipulate data in floating-point form, which greatly improves the efficiency of scientific computations.

### Addresses

Every memory address and every special register address in the Honeywell 800 has a unique numerical designation or address.  An instruction may refer to any memory location to obtain an operand or to store a result.  Unmasked general instructions and all shift instructions may refer to special registers, using memory designator bits to denote this type of addressing.  Masked general instructions do not have this ability.

A direct address is an explicit statement of the address of the desired operand.  An indexed address is written by specifying an index register and a quantity which augments the contents of this register to form the desired address.  (Eight index registers are included in each special register group.)  An indirect address is written by specifying a special register in which the desired address is stored, plus an increment which permanently alters the special register contents after use.  Six types of addresses may be written in the address groups of instructions.  A memory location or a special register may be addressed directly.  The augmented contents of an index register may be interpreted as a memory location address or as a special register address.  A memory location may be addressed indirectly by referring to a special register where the desired address is stored.  Finally, the special register used to obtain an indirect address may be specified by indexed addressing.  The ARGUS formats of these addressing options are presented in [Section V](#section-v-addresses).

The specifications of certain machine instructions direct that one or more address groups contain information other than references to memory locations or special registers.  Such information may include, for example, the number of words to be transferred, the number of positions to shift an operand, or the partial designation of a mask location.

### Masks

Reference to a word called a mask in an instruction permits the designation of partial words as operands and as a result.  The mask designates the character, digit, or bit positions within the operand words on which the stated operation is to be performed.  With certain of the general instructions (field instructions) the use of a mask is optional, but with shift instructions a mask is always required.

When an arithmetic operation is masked, the mask is applied to both operands and to the result.  Shift masks are applied after shifting and before delivery to the result location.  All masking in the Honeywell 800 leaves the unmasked portions of the result location unchanged (protected masking) except for the extract instruction (`EX`) and the two shift and extract instructions (`SWE` and `SPE`), which clear the unmasked portions of the result location to binary zeros (unprotected masking).

Masks are stored in the high-speed memory in groups of consecutive locations.  An instructions which uses a mask references the desired mask relative to an address known as the base of the mask group.  Each special register group includes a mask index register (`MXR`) which stores two mask group bases, according to a specified format: the base of a group of field masks and the base of a group of shift masks (see [Section X](#section-x-masking)).  The relative position of the desired mask within the group is specified in the instruction using the mask.  The base of a field mask group must be a multiple of 32 and the group includes up to 32 masks.  A field instruction can specify in its command code field any of the masks in this group.  The base of a shift mask group must be a multiple of 64 and the group includes up to 64 masks.  A shift instruction can specify in the `B` address field any of the masks in this group.  Therefore, each setting of the mask index register makes 96 memory locations available to the programmer for the storage of masks.  To conserve memory space by making certain masks available for use with either type of instruction, the two mask groups can be made to overlap.  With such an `MXR` setting, 64 memory locations are made available for the storage of masks, of which 32 can be used with field instructions and all 64 with shift instructions.

The programmer has the option of specifying the address of the desired mask in memory, or including information in the command code field which enables ARGUS to generate the desired mask (with the exception of the substitute (`SS`) and extract (`EX`) instructions, which always require a programmer-specified mask).

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
