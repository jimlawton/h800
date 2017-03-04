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

Programs to be assembled by ARGUS are written using the coding form shown in Figure 3.  The coding on these forms is then punched on standard 80-column cards according to the fixed-field format shown in Figure 4.  An instruction word occupies an entire line on the coding sheet and an entire punched card.  Constants may be combined, however, to allow punching of more than one on a single card.  When an entire program deck, complete with all necessary control instructions, is assembled by ARGUS, the program is produced in operating form on magnetic tape.  In addition, ARGUS produces a listing of the program in printed form.  Assembly outputs are described in [Section XII](#section-xii-output-from-argus-assembly-operation).

Figure 4 shows that the ARGUS input card contains seven fixed fields.  The function of each of these fields is described briefly in the following paragraphs.  The format of each input word type is illustrated in detail in the following sections.

### Location Field (Columns 1-10)

The location field may contain tags symbolizing memory locations, special registers, or masks.  Any word which is to be referred to symbolically in an address field of some other word, or which is to be loaded into a special register, or which is to be used as a mask, must include a tag in this field.  Tags may be punched anywhere in the location field; spaces are ignored.  The types and formats of tags are discussed in [Section IV](#section-iv-tags).

### Command Code (Columns 11-23)

The command code field is divided into two subfields.  Columns 11 through 22 contain the command code group itself, while column 23 designates the source of the next instruction.  If column 23 contains an "`S`" or if this column is blank, the next instruction will be taken from the sequence counter in the assigned special register group.  If column 23 contains a "`C`", the next instruction will be taken from the cosequence counter in this group.  This column is not used in a peripheral or a simulator instruction or in the instruction proceed (`PR`).

Columns 11 through 22 may contain the mnemonic operation code of a machine instruction, followed by any other information required by that instruction, as described in [Section VII](#section-vii-machine-instructions).  In the case of a constant, or set of constants, the command code field contains the constant code and any other required information, as described in [Section IX](#section-ix-constants).  This field may also be used to specify an ARGUS control instruction or the pseudo instruction of a library routine.  The formats of these words are described in Sections [VIII](#section-viii-assembly-control-instructions) and [XIII](#section-xiii-library-routines), respectively.

![Figure 3](images/figure_3.png?raw=true)

![Figure 4](images/figure_4.png?raw=true)

### Address Fields (Columns 24-37, Columns 38-51, Columns 52-65)

These three address fields correspond to the `A`, `B`, and `C` address groups of a Honeywell 800 machine instruction.  In a machine instruction, they may designate an operand location or a result location, using any of the six types of addresses permitted by the instruction.  These six address types are described in [Section V](#section-v-addresses).  In certain instructions, the address fields may contain instruction parameters or other information.  The three address fields are regarded as a single 42-column field for the purpose of punching constant words.  Their format in a library routine pseudo instruction is determined by the programmer who designs the library routine.

### Line Number (Columns 66-73)

Line numbers specify the sequence of words within a program.  When a new program is assembled, the cards may or may not contain line numbers.  If the cards do not contain line numbers, they must be read in correct sequence, as ARGUS assigns a line number to each card based on this sequence.  If the cards contain line numbers, ARGUS sorts the cards into proper sequence.

Line numbers are printed as part of the complete program listing produced by ARGUS.  They are used by the programmer in preparing additions, deletions, and corrections to assembled programs.  Five-digit line numbers are originally assigned the cards of a new program.  If assigned by the programmer, they are punched in columns 66 through 70.  To correct or replace one of the original cards of a program, the assigned five-digit number is punched in columns 66 through 70 of the modification card.  Columns 71 through 73 are used to insert additional cards in the correct sequence.  For example, if three cards are to be inserted in a program following card `01357` (according to the program listing), line numbers may be punched on the inserted cards as follows:

Column|66|67|68|69|70|71|72|73
------|--|--|--|--|--|--|--|--
Original Card|0|1|3|5|7|0|0|0
1st Insert|0|1|3|5|7|1|0|0
2nd Insert|0|1|3|5|7|2|0|0
3rd Insert|0|1|3|5|7|3|0|0
Original Card|0|1|3|5|8|0|0|0

Again at some later time, the programmer may insert additional cards following card `01357200` by numbering them `01357210`, `01357220`, etc.

### Identification (Columns 74-80)

These columns may contain a punch combination used to identify the cards of a related set of coding, such as a program segment.  If such codes are used as segment markers, for example, ARGUS can identify the segment to which each program card pertains.

### Remarks (Columns 66-80)

If either the line number or identification field (or both) is not used by the programmer, it may contain remarks.  Such information is not assembled but is reproduced for the programmer's convenience as part of the program listing.

A card containing only remarks may be included at any point in a program.  Such a card is indicated by and "`R`" or a "`P`" followed by a comma in columns 1 and 2 of the location field.  (`R` causes the remarks to be printed on the next line; `P` causes the remarks to be printed at the top of the next page.)  Remarks may be punched in all of the other columns (3-80) of a remarks card.

## Section IV: Tags

A tag punched in the location field of a program word allows the programmer to that word elsewhere in his program without being aware of its absolute location in memory.  A word may also be tagged to denote its use as a mask or to direct its storage in a special register.  Three groups of words must include a tag punched in the location field:
1. Certain of the words which are directly referenced in the address fields of other program words;
2. All words which are to be placed in special registers at loading time; and
3. All masks.
Tags may be punched anywhere in the location field; spaces are ignored.

### Symbolic Tags

A symbolic tag is a group of up to eight alphanumeric characters, of which at least one must be non-numeric.  However, there are certain characters which have significance to ARGUS and must not be included in symbolic tags.
Key Punch | Symbol | Machine Code
--------- | ------ | ------------
12 | `+` (plus) | `010000`
11 | `-` (minus) | `100000`
0, 8, 3 | `,` (comma) | `111011`
12, 8, 3 | `.` (period) | `011011`
11, 8, 4 | `*` (asterisk) | `101100`
0, 1 | `/` (slash) | `110001`
In addition, the following characters are not permitted within symbols even though they have no special significance.
Key Punch | Symbol | Machine Code
--------- | ------ | ------------
8, 4 | `-` (hyphen) | `001100`
11, 8, 5 | `"` (quotes) | `101101`
12, 8, 2 | `;` (semicolon) | `011010`
8,5 | ◊ (not assigned) | `110000`
0, 8, 7 | ⨂ (not assigned) | `111111`
Space codes (`001101`) within symbolic tags are ignored by assembly.

Tags are frequently chosen as mnemonic representations of the content or function of the tagged words, e.g., `GROSSPAY`, `INPUT1`, or `DIVIDEND`.  Such a tag may directly represent any location in the high-speed memory.  Every symbolic tag which appears in an address field within a program must appear in the location field within that program.

it is not necessary to tag every word of a program which is referenced by some other word.  Address arithmetic (described in [Section V](#section-v-addresses)) allows direct reference to an untagged word by specifying its location relative to a tagged word, e.g., `GROSSPAY + 2`.  The programmer decides which words of his program to tag and which to reference by address arithmetic.  Note that for purposes of assembly, address arithmetic is permitted only in an address field and never in the location field.<sup>1(#section-iv-note-1)

Normally every symbolic tag appearing in the location field is assigned an absolute value by ARGUS.  The program listing includes the assignment of each tag.  These assignments are used if the program is loaded independently, as is usually the case during program testing.  However, in production the program is generally loaded under the direction of Executive and the tag assignments are thereby modified to make the program compatible with any other programs being processed in parallel.

In addition to their use in referencing program words directly, symbolic tags may be used to represent other values, such as complete addresses in indexed or indirect form, or program parameters.  The programmer assigns the values of such tags using special ARGUS control instructions provided for this purpose.  These instructions, called `EQUALS`, `ASSIGN`, and `TAS` (temporary assign), are described in [Section VIII](#section-viii-assembly-control-instructions).

<a name="section-iv-note-1">1</a> PTS derail instructions are an exception to this rule, as described in the _ARGUS Program Test System Manual_, DSI-38.

### Special Register Tags

Each of the 32 special registers in a group has both an absolute address and a mnemonic designation.  The names and the absolute and mnemonic addresses of all special registers in a group are listed in Figure 5.  For example, this figure shows that the mask index register in any group may be designated absolutely as `07` or mnemonically as `MXR`.

A special register tag is required in the location field of every word to be loaded directly into a special register.  Such a tag consists of a "`Z`" followed by a comma and the absolute or mnemonic address of the desired register.  For example, either of the following special register tags
```
    Z,11
    Z,X3
```
might be used to load the tagged word into index register 3.  For a discussion of special register tags used in address fields, see [Section V](#section-v-addresses).

![Figure 5](images/figure_5.png?raw=true)

### Mask Tags

Every mask specified by the programmer must be designated in the location field by a unique symbolic tag.  These tags, like all symbolic tags used with ARGUS, can have up to eight alphanumeric characters, of which at least one must be non-numeric.  In addition, each such tag is preceded by a character which indicates that the corresponding mask is used with field instructions (`F`), shift instructions (`S`), or both (`B`).  Thus, a complete mask tag consists of a mask indicator followed by a comma and a symbolic tag.
```
    F,M3
    S,RIGHT2
    B,SIGN
```

### Link Tags

Any word which is to be the starting location of a segment (except the starting location of the first segment) should be so marked by tagging the word with a symbolic tag preceded by the letter "`L`" and a comma.

### Out-of-Sequence Words

It is sometimes convenient, particularly when writing macro routines, to have certain words places out of the main sequence of coding.  ARGUS recognizes any word marked by the letter "`X`" and a comma in the location field as an out-of-sequence word.  Such words are placed at the end of the subsegment in which they appear.  The "X," may or may not be followed by a symbolic tag.

ARGUS assigns out-of-sequence words by maintaining two location counters called `CLC` (current location counter) and `XLC` (out-of-sequence location counter).  Each counter is incremented after a word of the corresponding type is processed.  A word without "`X,`" in the location field is assigned to the location contained in the `CLC`.  A word with "`X,`" in the location field is assigned to the location contained in the `XLC`.

### Definition of Tags

When a tag appears in the location field of a line of coding, it becomes defined.  This results in the assignment of the tag to a memory location, an integer, or a complex address (i.e., an indexed address or a special register address).  A tag may have one absolute assignment (memory location or integer) or one complex assignment or one of each.  However, when a tag has conflicting assignments (e.g., two memory location assignments), it becomes doubly defined and is noted by ARGHUS as an error.  In general, such a conflict of assignment can arise only within a single segment.  In other words, a tag may have completely different assignments in the various segments of a program.  The only tags which must maintain their assignments throughout the entire program are link tags and tags which appear within the common portion of any segment (see [Section VI](#section-vi-program-structure)).

When a tag which has both an absolute assignment and a complex assignment appears in an address field, the complex assignment is normally used.  However, there are several exceptions to this rule, which are noted in connection with machine instructions, control instructions, and control constants.

## Section V: Addresses

In [Section II](#section-ii-the-honeywell-800-system), it was stated that every Honeywell 800 main memory location has a unique numerical designation, or address, consisting of a hexadecimal bank number from `0` to `G` and a subaddress from `0000` to `2047`.  It was stated further that each control memory location, or special register, is uniquely designated by a group number from `0` to `7` and a subaddress from `00` to `31`.

Most instructions can refer to any memory location or special register to obtain an operand or to store a result.  Three methods of addressing main and control memory are provided.  A direct address is a specific reference to the desired location or register.  An indexed address designates a special register called an index register, plus a quantity which augments the contents of the index register to form the desired address.  This process leaves the original contents of the index register unaltered.  An indirect address designates a special register in which the desired address is stored, plus an increment which permanently modifies the stored address after use.  The internal configurations of the various types of addresses are presented in the _Honeywell 800 Programmers' Reference Manual_ (DSI-31).  This section deals with their representation in ARGUS language, as summarized in Figure 6.

### Direct Memory Location Address

The programmer may directly reference a memory location by writing the symbolic tag assigned to that location in an address field.  ARGUS replaces this tag with the absolute address assigned.  Alternatively, the programmer may specify a direct memory location address by means of address arithmetic (see below).  Address arithmetic permits addressing relative to a tagged location or relative to one of the location counters (`CLC` and `XLC`) mentioned in [Section IV](#section-iv-tags).

Direct addressing may be used in an instruction to reference any location in the memory bank in which the instruction is stored.  An attempt to address any location outside of this bank results in an ARGUS error indication during assembly.  Therefore, the use of direct addressing is limited by the rules which govern relocation (see [Section VI](#section-vi-program-structure)).

![Figure 6](images/figure_6.png?raw=true)

#### Address Arithmetic

An address modifier, consisting of a sign and a number from 0 to 4095, may be appended to a symbolic tag to designate a direct memory location address relative to the location specified by the tag.  Such an address modifier may be appended to a "`C`" and a comma (`C,`) to designate a direct memory location address relative to the contents of the current location counter, or to an "`X`" and a comma to designate a direct memory location address relative to the contents of the out-of-sequence location counter.  Thus, the address
```
    ASSETS +37
```
is a direct reference to the memory location 37 beyond that represented by the symbolic tag `ASSETS`.  The address
```
    C,-3
```
refers to the memory location three before the location whose address is stored in the current location counter.  Likewise, the address
```
    X,+109
```
refers to the memory location 109 beyond the location whose address is stored in the out-of-sequence location counter.  The address modifier may be a series of numbers separated by the signs `+` and `-`, provided that the absolute value of the entire modifier does not exceed 4095.  Caution is required in the use of address arithmetic, since the address modifiers are not corrected if coding is inserted or deleted later.

Three types of direct memory location addresses are illustrated in the instruction
![Direct Address Example](images/address_example_p23.png?raw=true)
The function of this instruction is to add decimally the contents of the memory location two after the location of the instruction itself to the contents of the memory location designated by the tag `INTEREST`, and to store the result in the location 10 before that tagged `AMTPAID`.  (since this instruction is not marked by an "`X,`" in the location field, the CLC contains the address of this instruction while the instruction is being processed.)


The number of symbolic tags required to write a program can be greatly reduce by the use of address arithmetic.  The programmer decides how many and which words in a program to tag and which to reference by address arithmetic.

### Direct Special Register Address

The direct address of a special register is indicated by a "`Z`", a special register designation, and an unsigned increment from 0 to 31, all separated by commas.  The special register designation may be either the absolute subaddress (from 0 to 31) or the mnemonic address (e.g., `X3` or `MXR`) of the desired register, as shown in Figure 5, page 19.  If a special register is addresses as an operand location, the numeric increment is added, under control of the special register sign, to the special register contents, after those contents have been used.  If a special register is addressed as a result location, the increment is ignored.  To address a special register as an operand location without changing its contents, the programmer may omit the increment or may write an increment of `0`.

Any directly addressed special register is defined as being in the 32-register group controlling the program.  For example, 
```
    Z,X2,5
```
is the direct address of the second index register in the controlling special register group.  If it is used to specify an operand location, this address directs that the contents of `X2` are to be incremented by 5 after use.

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
