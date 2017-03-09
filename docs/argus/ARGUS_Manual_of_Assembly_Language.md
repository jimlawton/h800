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

```
            DA      C,+2    INTEREST    AMTPAID - 10
```
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

A special register group includes eight index registers, each capable of storing a sign, a bank indicator, and a memory location subaddress.  An indexed memory location address designates and index register and a quantity which augments its contents to form a complete memory location address.  The index register designator and the augmenter are separated by a comma.  The index register designator is a number from 0 to 7 which specifies one of the eight index registers in the controlling special register group.  Use of the letter "`X`" before the designator is optional.  The augmenter may be a number from 0 to 255 (254 for index register 7) or it may be a symbolic tag, with or without a modifier.  If symbolic, it must be assigned by an `EQUALS` instruction (see [Section VIII](#section-viii-assembly-control-instructions)) to a number which is a valid augmenter.  The computer forms a memory location address by adding the augmenter to the address stored in the index register, under control of the stored sign.  The unaugmented address is retained in the index register.

For example, the address `3,15` (or `X3,15`) specifies that the contents of index register 3 in the controlling group are augmented by 15 to form an absolute memory location address.  The address `7,DIVIDEND +2` specifies that the contents of index register 7 are augmented by 2 plus the quantity equated by the tag `DIVIDEND` to form the desired address.  If the sum of the augmenter plus the stored subaddress exceeds 2047, a carry occurs into the bank indicator and the resulting address will be in a different bank from the stored address.

Indexed addressing permits the programmer to address locations in any main memory bank, depending upon the value of the bank indicator stored in the index register.  This type of addressing may be used in processing multi-word items or in referring to a stored table.  The address of the first word in the item or table is stored in an index register and all references to the item or table are made using the index register designator with the appropriate augmenter.  To assure positive augmentation, the programmer must take care that the index register contains a positive sign.

### Indexed Special Register Address

An indexed special register address may be used to refer to a special register in any of the eight control memory groups.  Such an address takes the form:
```
    Index Register Designator, Z, Special Register Designator, Increment
```
The index register designator is a number from 0 to 7 (or `X0` to `X7`) which specifies one of the eight index registers in the controlling group.  The special register designator may be an absolute subaddress (`0`-`31`) or it may be mnemonic (see Figure 5).  The increment may be a number from `0` to `3` or it may be omitted.  The manner in which these numbers are used to augment the index register contents and form a special register address is illustrated in terms of bit structure.  ARGUS converts the address as written by the programmer to the following 12-bit configuration:

![Indexed Special Register Address Configuration](images/address_configuration_p25.png?raw=true)

Of this configuration, the low-order eight bits (increment, tabular bit, and special register designator) are added to the low-order eight bits of the index register contents, under control of the index register sign, permitting carry into the high-order bits.  As usual, the indexing process does not alter the contents of the index register.  The augmented index register contents are interpreted by the machine as a special register address, as follows:

![Special Register Address](images/special_register_p26.png?raw=true)

Within the augmented configuration, the group indicator and subaddress uniquely define a special register in any of the eight groups.  The increment is now a number from 0 to 31.  The tabular bit indicates whether the type of addressing is direct or indirect (see below).  In either case, the increment, under control of the special register sign, is added to the contents of the special register after use, provided the special register is not addressed as a result location.

If the index register used contains all zeros (except for the sign and the group indicator), the result of indexed special register addressing is quite simple.  In this case, the index register designates the group and the programmer designates the subaddress of a special register which is addressed directly and incremented after use by the amount which the programmer writes.  For example, assuming that the programmer writes
```
    3,Z,5,2
```
and that index register 3 contains
```
    +4,0,0,0
```
(group indicator of 4, increment, tabular bit, and special register subaddress of all zeros), the machine addresses special register 5 in group 4 directly and then increments its contents by `+2`.  However, if the index register contains more than a sign and a group indicator, the result of indexed special register addressing can only be understood by combining bit configurations as above.

### Indirect Memory Location Address

This address takes the form
```
    N, Special Register Designator, Increment
```
where the special register designator specifies a register in the controlling group absolutely or mnemonically, and the increment is a number from 0 to 31.  The machine interprets the contents of the specified register as the bank indicator and subaddress of a memory location which may be in any bank.  Whether the memory location is an operand or a result location, the increment is added to the contents of the special register, under control of the special register sign, after they have been used.  For example, the address
```
    N,R3,9
```
specifies the contents of special register `R3` in the controlling group, interpreted as an absolute memory location address.  After use, the contents of register `R3` are permanently modified by 9.

Indirect addressing is convenient for processing multi-item records when an operation is to be performed on word `M` of each item.  The location of word `M` of the first item is stored in a special register.  This location is then addressed indirectly, using an increment chosen to reset the special register to the location of word `M` of the second item.  Since the bank indicator of the memory location is derived from the special register, any memory bank may be addressed in this fashion.

### Indexed Indirect Memory Location Address

As noted in the discussion of indexed special register addressing, the augmented contents of an index register may be interpreted as a special register group indicator and subaddress, a tabular bit, and an increment.  If the tabular bit specifies indirect addressing, then the special register so designated is used to address a main memory location in any bank indirectly.  In this manner, any of the 256 special registers may be used to address any memory location indirectly.  This type of address, called an indexed indirect memory location address takes the form
```
    Index Register Designator, N, Special Register Designator, Increment
```
As with any other indexed address, the index register is one of the controlling group and is designated by a number from 0 to 7.  The special register designator may be absolute (from 0 to 31) or mnemonic, while the increment may be a number from 0 to 3 or may be omitted.  An address of this type is interpreted by the machine in the same manner as an indexed special register address, except that the 12-bit configuration formed by ARGUS contains a tabular bit of `1` to indicate indirect addressing.  The low-order eight bits of this configuration modify the low-order eight bits of the index register contents with carry, and the tabular bit in the result indicates whether the special register is addressed directly or used to address a memory location indirectly.  As with indexed special register addresses, it is simplest to use an index register containing only a sign and a group indicator and otherwise all zeros.  In this case, the special register and increment written by the programmer will be used and indirect addressing is assured.  If other information is stored in the index register, the eight-bit addition process may alter the tabular bit.  If this occurs, an `IR,N` address will produce the effect of an `IR,Z` address and vice versa.

Assume that the programmer writes the address
```
    3,N,AU1
```
and that index register 3 contains only a sign and a group indicator.  This group indicator and the mnemonic designator `AU1` define one of the 256 special registers, which is used to address a memory location indirectly.  Since no increment was written, the contents of the special register are left unchanged.

### Inactive Address

An inactive address is denoted in ARGUS language by a hyphen (`-`).  This type of address may be used to gain access to three non-addressable registers called the accumulator, the mask register, and the low-order product register.  In an addition instruction, for example, inactive addressing may be used to gain access to the accumulator.  If the `A` and `B` address groups are inactive, the contents of the accumulator are transferred to `C`; if the `B` and `C` address groups are inactive, the contents of `A` are transferred to the accumulator.  In similar fashion, inactive addressing may be used with the extract instruction to gain access to the mask register and with the transfer and sequence change (`TS`) instruction to gain access to the low-order product register.  Inactive addressing is discussed more fully in the _Programmers' Reference Manual_.

### Stopper Address

When a main memory address, stored in a special register, is modified by incrementing or augmenting, a carry may occur from the subaddress into the bank indicator.  Thus a sequencing counter can be stepped through successive memory banks, and a single instruction can handle a record which is not stored entirely within one memory bank.  There is one address, however, which by definition is neither incremented nor augmented when it appears in a special register.  This address, called the stopper address, represents the highest-numbered location in the memory of a given Honeywell 800 system, regardless of the number of banks in the system (i.e., subaddress `2047` in the highest-numbered bank of the system).  The stopper location can be utilized, for example, in a read instruction to move tape without disturbing the contents of memory or to read a portion of a tape record, discarding the balance.  Due to relocation considerations, the stopper location can only be addressed through a special register in ARGUS language.  This is accomplished by writing the symbolic tag `STOPPER` in a special address constant (see [Section IX](#section-ix-constants)) and storing it in a special register.  ARGUS replaces this tag with the address of the stopper location of the machine on which the program is to be run.

### Numbers in Address Fields

ARGUS will convert into binary any number or any series of numbers separated by the signs `+` and `-`, provided that the resultant value is positive and does not exceed `4095`.  This ability should be used with caution, especially if the program is to be relocated for parallel processing.

## Section VI: Program Structure

An assembled program may be divided into segments to conform to subdivisions of program logic.  This makes it possible to have the coding for one function in memory while the coding for other functions remains on tape until it is needed.  Segmentation makes efficient use of available memory storage and increases the number of programs that may be processed in parallel.  Segments may be further broken down into subsegments to increase the flexibility of relocation by the Executive System, to provide communication among segments, and to exercise control over the allocation of memory as performed by the Assembly Program.

### Segmentation

A segment is any part of a program which is loaded into memory and executed as a unit.  Segmented programs fall into two general categories.  One segment may operate upon the output of a previous segment with no internal communication, as in the case of a card-to-tape conversion which is followed by a sort and then by an updating run.  Such segments resemble a series of separate programs run one after another.  On the other hand, there may be communications among segments.  The communication link may be either a control program which decides what segment to load next, or an area of memory containing data which varies from segment to segment, or both.  Thus, unlike the first category, the order and frequency of executing the segments may not be predictable, but may depend upon the input data.

Programs in the first category are easily divided into mutually independent segments.  If these segments have different equipment requirements, they can be scheduled for production more efficiently if they are written as separate programs.  Programs in the second category, on the other hand, must be separated into interdependent and independent portions, according to the amount of memory available and the relative frequency of executing the various portions of coding.  The programmer uses the control instructions `PROGRAM` and `SEGMENT` (see [Section XI](#section-xi-argus-updating-function)) to segment a program.

Any part of any segment may be specified as "common" (as described below under "Subsegmentation").  When part of a segment is common, the area of memory which it uses is reserved in all segments.  It may be overlaid by common portions of other segments only under the programmer's control.  The portions of segments not specified as common, on the other hand, are overlaid by other segments under control of Executive.  In other words, the only parts of the program guaranteed to be in memory during the execution of one segment are those words belonging specifically to that segment and any common portions of other segments which occupy the communication area at the time.  For this reason, the symbolic tags defined in the common portions of a program may be referenced from any segment, while those not in a common area are available only to the segment in which they are defined.

### Segment Loading

The name of the first segment which is to be executed is specified on the `END` card (see [Section VIII](#section-viii-assembly-control-instructions)).  Executive automatically loads this segment when the program is initiated.  The starting address of this segment must be loaded into the sequence counter by means of a `SPEC` constant with "`Z,SC`" in the location field.

The programmer uses a macro instruction called read segment to direct the automatic loading of all segments following the first.  This instruction is logically equivalent to a transfer of control to that segment.  The Executive System loads the requested segment and transfers control to a location specified in the macro instruction, under control of the sequence counter.  Thus, no segment except the first one to be executed need load the sequence counter.  If a segment does load the counter, the address specified in the read segment instruction will override the one loaded.

The format of the read segment instruction is:

![Read Segment](images/read_segment_p30.png?raw=true)

```
    (TAG)   L,READSEG       NAME    START
```
"Name" is the segment name specified in the `PROGRAM` or `SEGMENT` card, and "start" is the symbolic tag of the location in that segment where control is to be transferred,  As in all macro instructions, the symbolic tag in the location field is optional.

The symbolic tag in the `B` address field must be a link tag, since it is referenced in one segment, while it actually belongs to another; this is an exception to the rule that all references within a segment must be to words within that segment or within the common area.  [Section IV](#section-iv-tags) states that a link tag is preceded by an "`L`" and a comma when it is defined.  Such a tag may be referenced from any segment, by means of the read segment macro instruction.  It should be noted that a reference to this tag from another segment must not include address arithmetic.  However, within the segment to which it belongs, this tag may be treated just as any other.

If desired, a segment may contain more than one starting location.  Each starting location must be designated by means of a link tag.  Different read segment macro instructions may be used to effect transfer of control to the different starting locations under various conditions.

### Subsegmentation

A subsegment is a group of words within a segment which must retain the same relationship to each other in memory; the relationship of one subsegment to other subsegments within the segment is immaterial.  Each segment may contain a maximum of seven subsegments.  The division of a segment into subsegments is indicated by means of the control instruction `SETLOC` (see page 53).  If no division is specified, the entire segment is considered to consist of one subsegment,

All subsegments of a segment occupy memory at the same time.  However, during relocation each subsegment may be moved in memory independently of the other subsegments with the following exceptions:
1. If any subsegment crosses a bank boundary, all subsegments of every segment within the entire program will retain their original relationships to each other and to the bank boundaries.  That is, the program is moved only by bank.
2. Two subsegments written to occupy the same memory bank will continue to share one memory bank unless one of the subsegments is in the communication area.  In this case, the subsegments may be moved into two different banks.
The programmer may reference any word in a subsegment from any other portion of the same segment, according to the following rules:
1. Any reference to a word in another bank must be made via a special register.
2. Unless some subsegment crosses a bank boundary (so that the program is relocated by bank), all references to the communication area from outside this area must be made via special registers.
3. Address arithmetic must not be applied to a tagged word in one subsegment in order to reference a word in another subsegment unless the program is relocated by bank.

One of the primary reasons for designating a portion of coding or data as a subsegment is to specify that it should be made common to all segments.  Subsegments not specified as common are called normal subsegments.  The normal subsegments of different segments are completely independent of each other; i.e., a subsegment numbered "`1`" in one segment bears no relation to a subsegment numbered "`1`" in another segment unless it is designated as common.  If a subsegment is designated as common, however, its number will refer to the same subsegment in all segments.

If a subsegment has been designated as common in one segment, words can be added to it or overlaid on portions of it by other segments.  The new words are preceded by a `SETLOC` instruction which states whether they are to be overlaid at a specified location or added at the end of the subsegment.

Another reason fir dividing a segment into subsegments is to increase the flexibility of relocation.  If two portions of a program (e.g., coding and data) need not occupy the same memory bank, it is desirable to code them as two subsegments, one in each of two banks.  Executive may then relocate them into any space which is available.

### Allocation

The Assembly Program assumes responsibility for the allocation of memory to a program; however, in some cases the programmer needs to have control over this allocation.  For example, in a multi-bank program he may wish to place his masks in a particular bank so that hey may refer to them directly from coding in that bank.

Each subsegment may contain any or all of these elements:
1. In-Line Coding - This consists of all program words except those which are designated as masks, loaded directly into special registers, or marked as out-of-sequence words.  As each in-line word is processed by the Assembly Program, it is assigned to the next available location in the subsegment.  Breaks in this sequence and/or initial values of this sequence may be specified by `SETLOC` instructions.
2. Out-of-Sequence Coding - This consists of all words in the subsegment which have "`X,`" in the location field (see page 20).  These words are assigned locations starting immediately after the in-line words of that subsegment.  Any subsegment which contains out-of-sequence coding should be stored entirely within one memory bank for ease of referencing such coding.
3. Masks - Masks are assigned in groups by means of the control instruction `MASKGRP` (see page 59).  This instruction may designate a subsegment in which the groups named are to be placed; otherwise, they are placed in the subsegment in control at the end of the segment.  If the `SETLOC` instruction for the subsegment containing the mask groups is immediately followed by a `SETLOC` for another subsegment, the mask groups will be allocated in a subsegment by themselves.
4. Subroutines - If a subroutine is called for within a common subsegment, it is stored within that subsegment; otherwise, it is stored in the subsegment in control at the end of the segment.  The programmer may use a `SETLOC` instruction immediately following the last line of a segment to specify the subsegment in which non-common subroutines are to be stored.  All subroutines stored in a subsegment are allocated immediately following the last location used in the subsegment.  The order in which subroutines are stored at the end of a subsegment is determined by the Assembly program on the basis of their size, and not on the order in which they are called or the order in which they appear in the library.

If a segment consists of more than 2048 words, so that it must occupy more than one bank of memory, it can be subsegmented in such a way that the out-of-sequence words and masks which are referenced by one section of coding will be stored in a bank with that coding.

### Relocation

Because a program is prepared without specific knowledge of the actual memory and equipment which will be assigned to it, certain precautions must be observed during program preparation to facilitate successful relocation and operation of the program.  Since the program will undoubtedly be run in parallel with others at some time, observance of the facts of relocation outlined below is also necessary in order that the program may not interfere with others.
1. The relocatable quantities - group and bank indicators and peripheral codes - should not be treated as numerical values.  In other words, no arithmetic operations should be performed on these quantities.
2. Although a one-to-one correspondence exists between group indicators of a program before and after relocation, this is not so with bank indicators.  Different bank indicators may be assigned the same value during relocation, since subsegments written for different banks may be loaded into the same bank at run time.  However, subsegments written for the same bank will always be assigned to the same bank, with the exception of common subsegments.
3. There is no relationship between bank indicators of different segments, except for common subsegments which remain in the same absolute areas throughout execution of the program.  Therefore, references between common and normal subsegments must be made via special registers.
4. Statements (2) and (3) above are limited to programs relocatable modulo 64, not to those relocatable by bank only.
5. Bank, group, and control unit indicators can be identified properly only if constants to be loaded into special registers are special address (`SPEC`) or complete address )`CAC`) constants (see [Section IX](#section-ix-constants)).
6. Fixed, non-relocatable locations (e.g., date location and inquiry stations) must be addressed via special registers.  The stopper location, which is represented by the tag `STOPPER` in a `SPEC` constant (see page 28), must also be addressed via a special register.
7. Because group indicators and tape control unit identifications are relocatable, care must be used in writing a program control constant to examine the program control register.  A program should examine only group and buffer bits used by that program.
8. The `MPC` instruction (see page 50) must be used with great care.  In particular, only those groups used by the program should be altered in any way.
9. The special registers `RAC`, `DRAC`, `WAC`, and `DWAC` are associated with control unit indicators and not with group indicators.  They must be addressed via special registers.  When they are addressed, control unit assignments must be uniquely defined.  It must be remembered that these counters may contain information from other programs using the same control unit.

In those control groups which contain the read-write counters `RAC`, `DRAC`, `WAC`, and `DWAC`, special registers `S4` through `S7` are not available.  Relocation is facilitated by always specifying a group in which these registers are unavailable, unless they are actually required by the program.  However, if a program does use any of the special registers `S4` through `S7`, it is the programmer's responsibility to specify a group in which these registers are available.  Further information on relocation can be found in the _ARGUS Executive System Manual_ (DSI-45).

#### Example

Two segments of a program have been assembled and allocated in memory as shown in the left-hand two columns of Figure 7 (Before Relocation).  Segment `A` consists of a common subsegment (numbered `1`) and four other subsegments.  Segment `B` consists of a common subsegment (which is also numbered `1`) and three other subsegments.  This program has been executed and checked out, using memory banks `0` through `3`, as shown.  Note that part of the common subsegment is loaded with segment `A` and part with segment `B` and that these parts are assigned overlapping memory areas.

The same program is to be loaded for processing in parallel with a number of other programs which are using memory banks `0`, `1`, and `4` through `G`.  When this program is scheduled for a production run, Executive examines its relocation information and relocates it as shown in the right-hand two columns of Figure 7 (After Relocation), so that it can be processed entirely within the available memory banks `2` and `3`.  A comparison of the two halves of Figure 7 reveals that the following rules govern the relocation process.
1. All subsegments are relocated in integral multiples of 64 locations to preserve all mask group relationships;
2. The two portions of common subsegment `1` retain the original overlapped relationship; and
3. Normal subsegments `2` and 4` of segment `A`, originally sharing the same memory bank, continue to share a bank after relocation.  These subsegments may communicate by means of direct addressing.  All other communication between subsegments must be by means of indirect addressing.

![Figure 7](images/figure_7.png?raw=true)

## Section VII: Machine Instructions

Honeywell 800 machine instructions are specified in ARGUS language using the mnemonic operation codes shown in Figure 8.  Note that ARGUS recognizes the five classes of machine instructions, namely, general, peripheral, shift, scientific, and simulator instructions, plus a group of extended instructions.  The functions of Honeywell 800 machine instructions re summarized in [Appendix E](#appendix-e-honeywell-800-machine-instructions).  The reader will find it convenient to refer to [Appendix E](#appendix-e-honeywell-800-machine-instructions) for the details of the machine instructions illustrated on the following pages.

A machine instruction consists of a command code group and three address groups.  The command code group may include such information as a mask tag or a peripheral code in addition to the mnemonic operation code, depending upon the instruction type.  An address group may refer to a memory location or a special register, using one of the address forms given in Figure 6, or it may contain a parameter dictated by the format of the instruction.  Information written either in the command code field, or in any address field may be punched anywhere in the indicated card field; spaces in these fields are ignored when assembling machine instructions.

### General Instructions

The instructions in this class perform such operations as arithmetic, information transfers, comparisons, program control, and information checking.  All of these instructions, with the exception of proceed, have the ability to designate the source of the following instruction.  If column 23 contains an "`S`" or is blank, the address of the next instruction is obtained from the sequence counter; if this column contains "`C`", the address of the next instruction is obtained from the cosequence counter.  Column 23 of a proceed instruction is not used, and the following instruction is always selected by the sequencing counter which selected the proceed instruction.

Three examples of general instructions are shown on the following page.  The first instruction adds the contents of location `PRICE` to the contents of the location three after `PRICE` and stores the result in location `AMTDUE`.  Both operands and the result are regarded as signed 11-digit decimal numbers.  The second instruction transfers 10 words from consecutive memory locations starting at `INPUT` to consecutive locations starting at `WORK1`.  The third compares numerically the contents of a memory location reached by indexed addressing with the contents of `COUNTER`.  If `(3,7)` is less than or equal to `(COUNTER)`, the cosequence counter is reset to the memory location 14 beyond the location of this instruction.  (Parentheses are used around an address to specify the contents of the indicated location.)  Each of the first two instructions is followed by an instruction selected by the sequence counter; the third instruction designates the cosequence counter as the source of the next instruction, whether or not the comparison is satisfied.  The functions of these three instructions can be verified by referring to [Appendix E](#appendix-e-honeywell-800-machine-instructions).

![General Examples](images/code_example_p38.png?raw=true)
```
            DA          PRICE       PRICE + 3       AMTDUE
            TN      S   INPUT       10              WORK1
            LN      C   3,7         COUNTER         C,+14
```

#### Sequence Change Instructions

Several instructions have the ability to execute a programmed change of sequence by placing the `C` address in the sequencing counter specified as the source of the next instruction.  An example is the transfer and sequence change instruction (`TS`).  In such instructions, the `C` address may take any valid address format.  However, if a special register is addressed, the value of the tabular bit is ignored and the result is always a memory location address.  Thus, a direct or indexed special register address, if used as a change of sequence, will be interpreted respectively as an indirect or an indexed indirect memory location address.

#### Field Instructions

Many of the instructions in the general class can be performed under the control of masks, which allow them to designate partial words as operands and as results.  These instructions, which are indicated by a superscript<sup>2</sup> in Figure 8 and in [Appendix E](#appendix-e-honeywell-800-machine-instructions), are called field instructions.  When a field instruction is masked, the same mask is applied to operands and results.  Only those bit positions in the operands which correspond to binary ones in the mask, called the masked portions are used.  All field instructions are masked protectively; i.e., the unmasked portions of the result locations are not altered by the operation.

The mask to be used in a field instruction may be designated by writing its symbolic tag in the command code field, following the operation code and separated from it by a comma.  A mask whose mask indicator is `F` (for field instructions) or `B` (for both field and shift instructions) may be designated in a field instruction.  If the tag which follows the operation code has both a mask assignment and a complex assignment, the mask assignment is used.  The method of assigning masks in groups of consecutive memory locations is described in [Section X](#section-x-masking).

![Figure 8](images/figure_8.png?raw=true)

Alternatively, the programmer may direct ARGUS to generate the desired mask.  The following three items of information in the command code field, separated from the operation code and from each other by commas, direct the generation of the desired mask by ARGUS:
- (M<sub>1</sub>) The position of the high-order character in the masked field.  This may be a number from `1` to `8` for alphanumeric characters, from `1` to `12` for unsigned hexadecimal digits, or from `2` to `12` for signed hexadecimal digits (see Figure 2).
- (M<sub>2</sub>) The number of characters in the masked field.  This may be a number from `1` to `8` for alphanumeric characters, from `0` to `11` for signed hexadecimal digits, or from `1` to `12` for unsigned hexadecimal digits.
- (M<sub>3</sub>) A character to specify the bit position(s) containing the sign of the masked field.  This character may be a number from `1` to `4`, corresponding to the four sign bits from left to right, or it may be an "`S`" to specify the use of all four as the sign of the masked field.  If the masked field is unsigned, as in alphanumeric information, this character is a `0` or is omitted.

The use of generated masks is limited to alphanumeric and hexadecimal fields of consecutive characters.  Tags must be used to designate masks for binary fields or for fields of non-consecutive characters.  The type of field, alphanumeric or hexadecimal, is implied by the operation code in most cases.  Arithmetic operations always involve numeric words and the comparison instructions specify numeric or alphabetic comparison.<sup>1(#section-vii-note-1)</sup>  In certain instructions, however, the type of field is ambiguous.  If one of these instructions (viz., `WA`, `WD`, `HA`, `TS`, `TX`, `SM` and `CP`) is to be performed with a generated mask, a three-character operation code must be formed by appending an "`A`" for alphanumeric or a "`D`" for hexadecimal to the two-character code shown in Figure 8.  Both designated and generated masks are illustrated in the following examples.

![Field Examples](images/code_example_p40.png?raw=true)
```
            DS,PAYROLL3     C   GROSSPAY    GROSSPAY - 3    NETPAY
            TXA,1,7             NAME                        PRINTOUT
            LN,2,B,S        S   TOTAL       DATA 1          COMPUTE
```

<a name="section-vii-note-1">1</a>In generating a mask for an alphabetic comparison, ARGUS assumes alphabetic operands.  If operands of such an instruction are numeric, any mask used must be designated by a symbolic tag.

The first instruction above subtracts decimally the contents of the location three before location `GROSSPAY` from the contents of location `GROSSPAY` and stores the result in location `NETPAY`.  Assume that the mask designated as `PAYROLL3` has the configuration
```
        G00 000 GGG GGG
```
in hexadecimal form.  This mask is applied to the subtraction operation, with the result that only the sign and the low-order six digits of each operand are considered and only those digit positions are affected in location `NETPAY`.

The second instruction transfers `(NAME)` to location `PRINTOUT`.  The contents of the command code field direct ARGUS to generate an alphanumeric mask of seven characters, starting with character one (the left-most character).  Thus only the first seven characters of `NAME` are transferred and the eight character position in location `PRINTOUT` is not altered.

The third instruction above compares `(TOTAL)` with `(DATA1)` numerically.  ARGUS generates a hexadecimal mask (because a numeric comparison is specified) which masks eight digits starting with digit `2`, the digit immediately following the sign.  All four bits of digit `1` are designated as sign bits.  If the masked portion of `TOTAL` is less than or equal to the masked portion of `DATA1`, the sequence counter (specified in the `S/C` column) is reset to `COMPUTE`.

Field instructions are subject to the restriction that when they are masked, they can neither address special registers nor use them to address main memory indirectly.  Consequently, they must obtain their operands and store their results by means of either direct or indexed addressing of memory locations.  This restriction does not apply to the remainder of the general instructions or to field instructions performed without masks.

#### N-word Instructions

Four general instructions which use the `B` address field to specify a number of words to be transferred (from 0-63) are the binary and decimal accumulate, n-word transfer, and multiple transfer instructions.  In any of these instructions, the `B` address field may contain a symbolic tag (with or without address modifier) which is equated elsewhere to a number, b=y means of an `EQUALS` instruction (see [Section VIII](#section-viii-assembly-control-instructions)).  The value of the tag (or the value of the modified tag) must be in the range `0` through `63`.  For example, if a block of data 20 words long is to be manipulated by several different n-word instructions, the tag `BLOCK` might be equated to the value `20`.  Then the following instruction could be used to transfer the data from locations starting with `INPUT` to locations starting with `OUTPUT`.
![N-Word Example](images/code_example_p42.png?raw=true)
```
            TN                  INPUT       BLOCK           OUTPUT
```

It is only necessary to modify the instruction which defines the tag `BLOCK`, rather than modifying all of the n-word instructions involved, if the length of the data block changes.

### Peripheral Instructions

Every instruction in this class performs some operation involving a ,magnetic tape unit or a terminal device.  Peripheral instructions are subject to the same addressing restrictions as masked field instructions.  They cannot specify a special register address or an indirect memory location address in any address field.  Furthermore, instructions in this class lack the provision for specifying the source of the following instruction.  Therefore, the `S/C` subfield (column 23) is not used in a peripheral instruction, and the address of the following instruction is always taken from the same sequencing counter that selected the peripheral instruction.

The command code field in a peripheral instruction contains a two-character operation code followed by a comma and an alphabetic peripheral code from `AA` to `HH`.  The assignment of peripheral codes to magnetic tape units and terminal devices is established individually at each Honeywell 800 installation.  In the case of a terminal device, the second letter of the peripheral code designates the device type, according to the following convention:
- `A` = card reader
- `B` = printer
- `C` = card punch
- `D` = paper tape reader
- `E` = paper tape punch
In the case of a magnetic tape unit, the second character may be any letter from `A` to `H`.  The Assembly Program uses this convention to analyze the peripheral requirements of a program and to diagnose and report any attempt to address a peripheral device which is not capable of performing the requested operation (e.g., a rewind addressed to a card reader).  Every Honeywell 800 installation is provided with a table of peripheral code assignments.

The `A` address field in a peripheral read or write instruction specifies the location into which the first word is top be read or from which the first word is to be written.  The read address counter (`RAC`) or the write address counter (`WAC`) directs the reading of subsequent word into or writing of subsequent words from consecutive higher-numbered locations until an end-of-record word is encountered (see [Appendix E](#appendix-e-honeywell-800-machine-instructions)).  (In a read backward instruction, the `RAC` directs the reading of subsequent words into consecutive lower-numbered locations.)

If the `B` address field in a read or write instruction to magnetic tape is active, the operation is a distributed read or write, and the record read or written is sensed for end-of-item symbols (see[Appendix E](#appendix-e-honeywell-800-machine-instructions)).  In this case, the `B` address field specifies the starting location of a stored table, which in turn contains the starting addresses of memory areas into which the items of a record are to be distributed or from which items are to be assembled to form a record.  The first item is read or written, starting at `A`; subsequent items are read or written starting at the addresses stored in the table.  The distributed read address counter (`DRAC`) or the distributed write address counter (`DWAC`) directs the selection of addresses from the stored table to distribute or assemble the items of a record.  (If a read backward is distributed, the `B` address field specifies the final location of a stored table of final addresses of items.)  If the `B` address field is inactive, the operation is a normal read or write, end-of-item symbols are not sensed, and the `DRAC` and `DWAC` are not used.

The `C` address field in any read or write instruction may be used to specify a change in the contents of the sequencing counter which selected the instruction; if the `C` address field is inactive, no change of sequence takes place.  If the `C` address is active, it is interpreted as in any other sequence change instruction (see above).

If the `A` address field in a rewind instruction is active, the rewound tape is interlocked against further peripheral operations.  The `B` and `C` address fields in a rewind instruction are not used.

![Read-Write Examples](images/code_example_p43.png?raw=true)
```
            WF,FB               UPDATE      -               READIN + 2
            RF,AB               TRANSACT    WORK 3          -
```

The function of the first instruction above is to write one record or print one line on device `FB`, depending upon whether this device is a magnetic tape unit or a printer.  The record to be written is stored in memory starting at location `UPDATE`.  Since the `B` address field is inactive, end-of-item symbols are not sensed; i.e., the records is assumed to be stored in consecutive memory locations.  The `C` address field designates that the counter which selected this instruction is to be set to address `READIN +2`.

The second sample instruction reads one record from device `AB`.  The record is to be stored in memory, the first item starting at location `TRANSACT`.  `WORK3` is the first location of a stored table of starting addresses of items.  As the record is read, end-of-item symbols are sensed, and the `RAC` and `DRAC` control distribution of the remaining items to non-consecutive memory areas.  As terminal devices cannot perform distributed reading, `AB` must be a magnetic tape unit.  Since the `C` address field is inactive, the sequencing counter which selected this instruction is incremented normally to form the address of the next instruction.

### Shift Instructions

Four of the five shift instructions are used to alter the positions of data fields within words.  Two of these substitute the shifted field into a word which is otherwise unaltered; the other two extract the shifted field into a word which is otherwise cleared to all zeros.  The fifth instruction, shift and select, is used to select one of a possible 2048 locations as the source of the following instruction, based upon the value of a data field.

Every shift instruction is performed under the control of a mask.  The location of the word to be shifted is written in the `A` address field.  The type, extent, and direction of the shift are specified in the `B` address field.  All five instructions perform end-around shifting; i.e., every character shifted out of a word at one end reappears at the opposite end.  The shifted word is masked and then delivered to the location specified by `C` (or used to modify the `C` address in the shift and select instruction).  The two shift and substitute instructions protect the unmasked portions of the result location.  The two shift and extract instructions clear the unmasked portions of the result location to all binary zeros.  As in the case of field instructions, the desired mask may be either designated symbolically or generated by ARGUS.  The tag of a designated mask is written in the command code field of the shift instruction, following the operation code and separated from it by a comma.  A mask with a mask indicator of `S` (for shift instruction) or `B` (for both) may be designated in a shift instruction.  If the tag written has both a mask assignment and a complex assignment, the mask assignment is used.  To generate a mask, ARGUS uses the same three items of information (M<sub>1</sub>, M<sub>2</sub>, and M<sub>3</sub>) as outlined under field instructions.  M<sub>1</sub>, M<sub>2</sub>, and M<sub>3</sub> follow the operation code and are separated by commas.  Since shifting takes place before masking, M<sub>1</sub> must specify the position of the high-order character in the masked field _after_ shifting.  The shift word and the shift and select instructions do not normally include a value of M<sub>3</sub>.

Any valid address format, as shown in Figure 6, may be used in the `A` and `C` address field of a shift instruction.  However, the `C` address field of a shift and select instruction is interpreted as in any other sequence change instruction (see page 38).  The `B` address field of a shift instruction normally contains three items of information, separated by commas, which specify the nature and extent of the shift:
- (`B`<sub>1</sub>) A character to designate the type of characters to be shifted.
    - `A` = six-bit alphanumeric
    - `D` = four-bit decimal
    - `B` or blank = binary
- <sup>*(#section-vii-note-2)</sup>(`B`<sub>2</sub>) The number of positions that the word is to be shifted, from `0` to `8` for alphanumeric characters, from `0` to `12` for decimal digits, or from `0` to `48` for bits.
- (`B`<sub>3</sub>) A character to designate the direction of shift.
    - `L` = left
    - `R` or blank = right
Alternatively, the `B` address field may contain a symbolic tag (with or without address modifier) which is equated elsewhere to a number, by means of an `EQUALS` instruction (see [Section VIII](#section-viii-assembly-control-instructions)).  The value of the tag (or of the modified tag) must be in the range `0` through `48`.  ARGUS interprets such a tag as the number of bit positions to be shifted to the right.

<a name="section-vii-note-2">*</a>If `B`<sub>1</sub> and `B`<sub>3</sub> are both blank, `B`<sub>2</sub> may be as large as `63`.

As in the case of field instructions, the use of generated masks is limited to alphanumeric and decimal fields of consecutive characters.  Masks for binary fields or for fields of non-consecutive characters must be designated symbolically.  If no mask information is written in the command code field and the shifted field is alphanumeric or decimal (`B`<sub>1</sub> = `A` or `D`), ARGUS generates a mask to suppress that portion of the word moved either right or left end around during the shifting process.  However, if `B`<sub>1</sub> specifies a binary shift or the `B` address field is symbolic, ARGUS generates a mask of all ones in the absence of a mask tag in the command code field.  The shift and select instruction requires a mask which allows no more than 11 low-order bits to be used in modifying the `C` address.

![Shift Examples](images/code_example_p45.png?raw=true)
```
            SPS,PARTNUMB    S   3,9         B,10,R          PART LIST +5
            SWE,6,3             EMPLOYEE+4  D,3             N,R3,1
            SSL,11,2        C   SELECTOR    D,4             C,-5
```

The first sample instruction above shifts the contents of the location specified by indexed address `3,9` ten binary places to the right, preserving the sign, and stores the result in location `PARTLIST +5`, under control of a mask tagged `PARTNUMB`.  The unmasked portion of the result location is protected.  The sequence counter is consulted for the source of the next instruction.

The second instruction shifts the contents of location `EMPLOYEE +4`, including the sign, three decimal places to the right (`B`<sub>3</sub> is blank) and stores the result in the location specified by indirect address `N, R3, 1`.  The generated mask produces an unsigned field of three decimal digits beginning with digit 6 and replaces the remainder of the result location with all `0` bits.  Again the sequence counter is consulted for the source of the next instruction.

The third instruction shifts the contents of location `SELECTOR`, including the sign, four decimal places to the right under control of a generated mask which produces a field of two low-order decimal digits.  These eight bits are added in binary form to the address of a memory location five before the location of this instruction (since this is not marked as an out-of-sequence word).  The modified address is then stored in the cosequence counter which is designated as the source of the next instruction.

### Scientific Instructions

This class includes the instructions which perform arithmetic operations and comparisons on floating-point numbers.  Figure 2, page 8, shows that a Honeywell 800 floating-point word consists of a 40-bit mantissa, a seven-bit exponent, and a sign bit.  This configuration may represent either a decimal number or a binary number in floating-point form.  Arithmetic instructions are provided to handle floating-point words either as decimal or as binary numbers.  Data which is to be manipulated in floating-point form is normally assembled in this form, using the floating-point binary and floating-point decimal constants described in [Section IX](#section-ix-constants).  However, fixed-point binary and decimal constants can be converted to floating-point form.  In normalized floating-point decimal, the exponent represents a power of 10 from the -64<sup>th</sup> to the +63<sup>rd</sup> and the mantissa a 10-digit number from `.1000` to `.9999----`.  In normalized floating-point binary form, the exponent represents a power of 16 from the -64<sup>th</sup> to the +63<sup>rd</sup> and the mantissa a 40-bit number from `.00010000----` to `.11111111----`.  n exception is the value `0`.  Although any floating-point number whose mantissa is `0` has the value of `0`, a normalized floating-point `0` in the Honeywell 800 is defined as a number having a positive sign and all binary zeros in the exponent and the mantissa.

The operands used in a floating-point instruction must be in floating-point form but not necessarily normalized (with the exception of divisors and operands for the comparison instructions).  The results are in correct floating-point form, and are normalized except where otherwise specified.  Exponential overflow occurs if the exponent of the result exceeds `+63`; exponential underflow occurs if the result exponent is less than `-64`.  When exponential overflow is sensed, an unprogrammed transfer of control to `U + 14` or `U + 15` is executed, where `U` represents the location whose address is stored in the unprogrammed transfer register (see Figure 5, page 19).  When exponential underflow is sensed, the unprogrammed transfer is to `U + 12` or `U + 13`.

A floating-point divide instruction cannot be executed if the possibility exists that the divisor is 0.  A fixed-point divide instruction cannot be executed if the absolute value of the quotient equals or exceeds unity.  In either case, an unprogrammed transfer of control to `U + 10` or `U + 11` is executed.

The machine logic to implement the scientific instructions is an optional feature of the Honeywell 800.  Included in this option are the two fixed-point divide instructions.  Though none of these can be performed as machine instructions on systems which do not include the floating-point option, they are all represented by library routines which can be performed by such systems.  One of the items of input required by ARGUS is an indication of whether or not programs are to be assembled for a system which includes the floating-point option (see [Section XI](#section-xi-arhus-updating-function)).  In assembling programs for such a system, scientific instructions are assembled as machine instructions; otherwise, they are handled as library routine pseudo instructions (as described in [Section XIII](#section-xiii-library-routines)).

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
