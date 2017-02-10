# HONEYWELL 1800 
## Programmers' Reference Manual

Honeywell Electronic Data Processing

Price . . . . . $4.00

Questions and comments regarding this manual should be addressed to:

    Honeywell Electronic Data Processing
    Merchandising Division
    60 Walnut Street
    Wellesley Hills, Massachusetts 02181

FIRST EDITION
First Printing, May, 1963
Second Printing, June, 1964

Copyright 1964
Honeywell Inc.
Electronic Data Processing Division
Wellesley Hills, Massachusetts 02181

## FOREWORD

The purpose of _The Programmers' Reference Manual_ is to define the internal machine language of the Honeywell 1800 Electronic Data Processing System and 
the manner in which that language is interpreted and manipulated by the system.  This manual is not intended to be either an introduction to programming or an introduction to the Honeywell 1800.  Instead, it is written as a handbook for the experienced programmer who has completed the Honeywell 1800 (or 800) programming course.

Throughout the manual the phrase "the performance of the system is unspecified" refers to instruction configurations whose results cannot be predicted from one execution to another.

## NOTE

This is the second printing of _The Programmers' Reference Manual_.  The principal differences between this and the first printing are as follows.

1.  The discussion of input/output traffic control (pp. 18ff) has been clarified.
2.  A new Appendix F discusses the extension of main memory beyond 32,768 words.
3.  A new Appendix G describes the memory barricade feature.

## TABLE OF CONTENTS

```
                                                                           Page
  Section I     Introduction ..............................................   1
                    Programming Aids ......................................   1
                    Fixed-Point Numbers ...................................   2
                    Decimal System ........................................   2
                    Binary System .........................................   2
                    Binary Codes ..........................................   3
                    Octal and Hexadecimal Systems .........................   3
                    Floating-Point Numbers ................................   3

  Section II    The Honeywell 1800 System .................................   5
                    The Equipment .........................................   5
                        1.  The Central Processor .........................   5
                        2.  The Floating-Point Option .....................   6
                        3.  The Console ...................................   6
                        4.  Magnetic Tape Units and Tape Controls .........   7
                        5.  The Card Equipment ............................   8
                            a.  Card Readers ..............................   8
                            b.  Card Punch ................................  11
                            c.  Card Reader - Card Punch ..................  11
                        6.  The Printers ..................................  12
                            a.  Standard-Speed Printers ...................  12
                            b.  High-Speed Printer ........................  12
                        7.  The Paper Tape Equipment ......................  13
                            a.  Paper Tape Reader and Control .............  13
                            b.  Paper Tape Punches and Controls ...........  14
                        8.  Off-Line Controls .............................  15
                        9.  Additional Equipment Available in the Honeywell
                             1800 System ..................................  16
                            a.  Random Access Storage and Control .........  16
                            b.  Optical Scanning Unit and Control .........  16
                            c.  Communications Control ....................  16
                            d.  Tape Control ..............................  16
                            e.  Magnetic Tape Switching Unit ..............  16
                            f.  Real-Time Control Units ...................  17
                            g.  Programmed Elapsed Time Clock .............  17
                            h.  Programmed Real Time Clock ................  17
                            i.  Honeywell 1800 III ........................  17
                    Traffic Control .......................................  17
                    System Configurations .................................  21
                    Multiprogram Control ..................................  22
                    Orthotronic Control and Checking ......................  24

  Section III   The Honeywell 1800 Word ...................................  27
                    Data Words ............................................  27
                    Special Register Words ................................  29
                    Instruction Words .....................................  29
                    General Instructions ..................................  30
                    Unmasked General Instructions .........................  30
                    Masked General Instructions ...........................  31
                    Inherent Mask Instructions ............................  32
                    Peripheral and Print Instructions .....................  32
                    Simulator Instructions ................................  33
                    Scientific Instructions ...............................  33
                    Special Words .........................................  34

  Section IV    Addressing ................................................  35
                    Direct Memory Location Address ........................  36
                    Direct Special Register Address .......................  37
                    Indexed Memory Location Address .......................  39
                    Indexed Special Register Address ......................  40
                    Indirect Memory Location Address ......................  41
                    Indexed Indirect Memory Location Address ..............  43
                    Summary of Address Forms ..............................  44
                    Significant Main Memory Addresses .....................  44
                    Stopper Address .......................................  46
                    Inactive Addresses ....................................  47

  Section V     Special Registers .........................................  51
                    Sequencing Counters ...................................  54
                    History Registers .....................................  56
                    Index Registers .......................................  56
                    Mask Index Register ...................................  57
                    General Purpose Registers .............................  58
                    Read-Write Counters ...................................  58
                    Arithmetic Control Counters ...........................  60
                    Unprogrammed Transfer Register ........................  61

  Section VI    Arithmetic Instructions ...................................  65
                    The Accumulator .......................................  65
                    The Low-Order Product Register ........................  67
                    Binary Add, BA ........................................  67
                    Decimal Add, DA .......................................  68
                    Binary Subtract, BS ...................................  69
                    Decimal Subtract, DS ..................................  69
                    Word Add, WA ..........................................  69
                    Word Difference, WD ...................................  70
                    Binary Accumulate, BT .................................  70
                    Decimal Accumulate, DT ................................  71
                    Binary Multiply, BM ...................................  71
                    Decimal Multiply ......................................  72

  Section VII   Logical Instructions ......................................  75
                    Extract, EX ...........................................  75
                    Substitute, SS ........................................  76
                    Half Add, HA ..........................................  77
                    Superimpose, SM .......................................  77

  Section VIII  Transfer Instructions .....................................  79
                    Transfer A to C, TX ...................................  80
                    Transfer and Sequence Change, TS ......................  80
                    N-Word Transfer, TN ...................................  81
                    Multiple Transfer, MT .................................  82
                    Record Transfer, RT ...................................  83
                    Item Transfer, IT .....................................  83

  Section IX    Decision Instructions .....................................  85
                    Inequality Comparison, Alphabetic, NA .................  86
                    Less Than or Equal Comparison, Alphabetic, LA .........  87
                    Inequality Comparison, Numeric, NN ....................  87
                    Less Than or Equal Comparison, Numeric, LN ............  87

  Section X     Shift Instructions ........................................  89
                    Shift Preserving Sign and Substitute, SPS .............  91
                    Shift Preserving Sign and Extract, SPE ................  91
                    Shift Word and Substitute, SWS ........................  91
                    Shift Word and Extract, SWE ...........................  92
                    Shift Word and Select, SSL ............................  92

  Section XI    Peripheral Instructions ...................................  95
                    Read Forward, RF ......................................  97
                    Read Backward, RB ..................................... 100
                    Write Forward, WF ..................................... 102
                    Rewind, RW ............................................ 105

  Section XII   Miscellaneous Instructions ................................ 107
                    Print, PRA, PRD, PRO .................................. 107
                    Control Program, MPC .................................. 109
                    Proceed, PR ........................................... 114
                    Simulator, S .......................................... 114
                    Compute Orthocount, CC ................................ 116
                    Check Parity, CP ...................................... 117

  Section XIII  Scientific Instructions ................................... 121
                    Floating-Point Numbers ................................ 121
                    Floating-Point Arithmetic Registers ................... 121
                    Instruction Configurations ............................ 123
                    Inactive Addresses .................................... 124
                    Exponential Overflow and Underflow .................... 125
                    Checking .............................................. 126
                    Floating Binary Add, FBA .............................. 127
                    Floating Binary Subtract, FBS ......................... 127
                    Floating Decimal Add, FDA ............................. 127
                    Floating Decimal Subtract, FDS ........................ 127
                    Floating Binary Add, Extended Precision, FBAE ......... 127
                    Floating Binary Subtract, Extended Precision, FBSE .... 127
                    Normalized Floating-Point Addition and Subtraction .... 128
                    Unnormalized Floating-Point Addition and Subtraction .. 128
                    Floating Point Binary Add, Unnormalized, FBAU ......... 128
                    Floating Point Binary Subtract, Unnormalized, FBSU .... 129
                    Floating Point Decimal Add, Unnormalized, FDAU ........ 129
                    Floating Point Decimal Subtract, Unnormalized, FDSU ... 129
                    Timing Notes on Floating-Point Addition and Subtraction 129
                    Floating Binary Multiply, FBM ......................... 129
                    Floating Decimal Multiply, FDM ........................ 130
                    Timing Notes on Floating-Point Multiplication ......... 130
                    Floating Binary Divide, FBD ........................... 130
                    Floating Decimal Divide, FDD .......................... 131
                    Fixed Binary Divide, BD ............................... 131
                    Fixed Decimal Divide, DD .............................. 131
                    Timing Notes on Division .............................. 132
                    Normalized Less Than Comparison, FLN .................. 132
                    Normalized Inequality Comparison, FNN ................. 133
                    Fixed-to-Floating Normalize, FFN ...................... 133
                    Multiple Unload, ULD .................................. 134
                    Conversion, FCON ...................................... 134

  Section XIV   Summary of Instructions ................................... 137
                    General Instructions, Unmasked or Masked .............. 137
                    General Instructions, Unmasked ........................ 138
                    Inherent Mask Instructions ............................ 139
                    Peripheral and Print Instructions ..................... 140
                    Simulator Instructions ................................ 141
                    Scientific Instructions ............................... 141

  Appendix A.   Fixed-Point Addition in the Honeywell 1800 ................ 145

  Appendix B.   Orthotronic Control ....................................... 149

  Appendix C.   Timing Summary ............................................ 155

  Appendix D.   Control Errors ............................................ 165

  Appendix E.   Tables .................................................... 167

  Appendix F.   Memory Extensions beyond 32,768 Words ..................... 169

  Appendix G.   Memory Barricade .......................................... 173
```

## LIST OF ILLUSTRATIONS

```
Figure   II-1.  Conversion of Punch Positions to Honeywell 1800 Character
                    Positions .............................................  10

Figure   II-2.  Stages of Traffic Control .................................  19

Figure  III-1.  Honeywell 1800 Word Structure .............................  28

Figure  III-2.  Honeywell 1800 Major Instruction Types ....................  31

Figure   IV-1.  Main Memory Address .......................................  35

Figure   IV-2.  Special Register Address ..................................  35

Figure   IV-3.  Direct Memory Location Address ............................  37

Figure   IV-4.  Direct Special Register Address ...........................  38

Figure   IV-5.  Indexed Memory Location Address ...........................  39

Figure   IV-6.  Indexed Special Register Address ..........................  41

Figure   IV-7.  Indirect Memory location Address ..........................  42

Figure   IV-8.  Interpretation of Address Bit Structure ...................  45

Figure    V-1.  Special Register Names, Subaddresses and Mnemonic Addresses  52

Figure    V-2.  Mask Index Register .......................................  57

Figure    V-3.  Generated Mask Address in Shift Instructions ..............  57

Figure    V-4.  Generated Mask Address in Field Instructions ..............  58

Figure    V-5.  Unprogrammed Transfers of Control .........................  62

Figure  XII-1.  Honeywell 1800 Special Register Group Indicator 
                    Relationships ......................................... 112

Figure  XII-2.  B Address Group Function in Control Program Instruction ... 113

Figure  XII-3.  Bit Layout - Memory and Tape .............................. 119

Figure XIII-1.  Exponent Ranges in the Floating-Point Option .............. 126

Figure XIII-2.  Timing of Floating Add and Subtract Instructions .......... 129

Figure XIII-3.  Timing of Floating Multiply Instructions .................. 130

Figure XIII-4.  Timing of Fixed and Floating Divide Instructions .......... 132

Figure    A-1.  Schematic Representation of Bus and Accumulator ........... 146

Figure    B-1.  Relation of Data Words to Orthowords ...................... 150

Figure    B-2.  Computation of Orthowords ................................. 150

Figure    B-3.  Orthotronic Check of Tape Error ........................... 151

Figure    B-4.  Orthocount of Error Record ................................ 152

Figure    B-5.  Correction of Tape Error - First Method ................... 153

Figure    B-6.  Correction of Tape Error - Second Method .................. 153

Figure    D-1.  Control Error Bit Configurations .......................... 165

Figure    G-1.  Partitioning of Memory by the Barricade ................... 175

Figure    G-2.  Limited and Critical Control Errors ....................... 177

Table       I.  Honeywell 1800 Coding and Punched or Printed Equivalents .. 167

Table      II.  Honeywell 1800 Command Codes .............................. 168
```

## SECTION I

### INTRODUCTION

The Honeywell 1800 Electronic Data Processing System is designed to handle large-scale business and scientific applications.  Its ability to deal efficiently with such applications derives from the provision of large main memory capacity (up to 65,536 twelve-digit words), high computational speed (e.g., 125,000 three-address additions per second), automatic parallel processing of up to eight independent programs, high-speed magnetic tape input and output (133,300 decimal digits/second per magnetic tape unit), and optional floating-point arithmetic.  The system is fully compatible with the Honeywell 800 in programming logic, input/output capabilities, and general physical and environmental characteristics.

#### Programming Aids

Every Honeywell 1800 user is furnished with a complete automatic programming package which eliminates many of the routine human tasks involved in program preparation, checkout, and execution.  This package includes the following compatible elements:

1.  ARGUS, the H-800 assembly system which includes subroutine capabilities, sort and collate generators, and a program test facility for obtaining diagnostic information about a series of unchecked programs during automatic, full-=speed execution.
2.  COBOL, the COmmon Business Oriented Language which facilitates the interchangeability among various computers of programs prepared in a narrative language closely resembling everyday business english.
3.  FACT, a powerful, English-language compiler developed especially to facilitate the programming of business applications for the H-800.
4.  Automath, the scientific counterpart of COBOL and FACT.  Automath interprets a series of problem statements in a FORTRAN-comparable arithmetic and logical notation and produces a complete machine-language program specifically directed to the solution of a program in the scientific area.
5.  A library of thoroughly tested subroutines and macro routines for inclusion in compiled or assembled programs, and a program (LAMP) to maintain it.
6.  ADMIRAL and Executive, two sophisticated monitoring systems which direct the operation of multi-program runs to facilitate maximum usage of the benefits of Honeywell automatic parallel processing.

The extent and power of this automatic programming package permit programs to be prepared for the Honeywell 1800 without reference to the language set forth in the _Programmers' Reference Manual_. In other words, the ARGUS _Manual of Assembly Language_, and the COBOL, FACT, and Automath Compiler manuals are the standard programming documents for the Honeywell 1800.  Nevertheless, this manual is offered for use by the sophisticated programmer who is eager to take advantage of the unusual and powerful features of the machine.  When this level of experience is reached, an understanding of the internal configurations of instructions and data, as presented in the following sections, will prove invaluable.

Throughout this manual, the binary-digit structure of instructions and addresses is presented wherever it can enhance the explanation.  Moreover, other numbering systems, such as octal and hexadecimal, are utilized wherever the subject matter requires them.  For comparative purposes, the ARGUS format of many examples is also shown.

#### Fixed-Point Numbers

Most numbering systems in general use today are based on positional notations.  This means that each system is based on a root number, called the radix, and that each position within a number represents a specific power of the radix of the particular system being used.  Positive and negative powers of the radix are separated by an indicator point (the radix point), with the zero<sup>th</sup> power of the radix appearing immediately to the left of the point.  Positive powers of the radix appear in successive positions to the left and negative powers in successive positions to the right of the indicator point.  The radix of a numbering system is equal to the number of digits comprising that system; these digits cover the range from zero to one less than the radix.  Numbers written in positional notation are called fixed-point numbers.

#### Decimal System

The familiar decimal system is based on a radix of 10 and uses 10 digits from 0 through 9.  Each position in a fixed-point decimal number represents a specific power of 10 and can have any of 10 values.  The total value of a fixed-point decimal number is computed by multiplying the value of each digit by the positional value (power of 10) of its position within the number and then summing all of these products.  For example, the decimal number 356. has the value 3 x 10<sup>2</sup> plus 5 x 10<sup>1</sup> plus 6 x 10<sup>0</sup>, or 300 + 50 + 6.  The number 3.56 has the value 3 x 10<sup>0</sup> plus 5 x 10<sup>-1</sup> plus 6 x 10<sup>-2</sup>, or 3 + 5/10 + 6/100.  When positional notation is understood in the familiar decimal context, the interpretation of any other positional system becomes clear.

#### Binary System

This system is based on a radix of 2 and uses the two binary digits (or bits) 0 and 1.  Binary numbers are the common internal system for digital computation due to the relative simplicity of recording, storing, and recognizing variables of only two values.  The value of a fixed-point binary number is computed by multiplying the value of each digit by the corresponding power of 2 and summing all the products.  For example, the binary number 1001 has the value 1 x 2<sup>3</sup> plus 0 x 2<sup>2</sup> plus 0 x 2<sup>1</sup> plus 1 x 2<sup>0</sup>, or 8 + 0 + 0 + 1, which equals 9.  Where the system in use is not made clear by the context, its radix may be appended to the number as a subscript as, for example, to distinguish the binary number 1001<sub>2</sub> from the decimal number 1001<sub>10</sub>.

#### Binary Codes

In addition to the use of "pure binary" numbers, as described in the preceding paragraph, binary digits may be grouped so that each group represents a decimal digit, alphabetic character, or other symbol.  For example, bits may be manipulated in groups of four with each group representing a decimal digit (from 0000<sup>2</sup> to 1001<sup>2</sup>).  Similarly, groups of six bits may represent up to 64 digits, characters, or symbols.  Such 4-bit and 6-bit codes are called "binary-coded decimal" and "alphanumeric," respectively.  They facilitate the handling of the external decimal and alphabetic symbols by machine elements which recognize only variables of two values.

#### Octal and Hexadecimal Systems

The octal system and the hexadecimal system, based on radices of 8 and 16, respectively, are useful as shorthand methods of writing pure binary numbers.  If a binary number is divided into groups of three bits, proceeding in either direction from the indicator point, each group may be replaced directly by its octal equivalent, since a 3-bit group has a total of eight possible values.  If the same number is divided into 4-bit groups in the same manner, each group may be replaced directly by its hexadecimal equivalent, since a 4-bit group has a total of 16 possible values.  The 16 hex digits are represented in this manual by the symbols 0 - 9 and B - G, respectively.

#### Floating-Point Numbers

It can be seen from the foregoing discussion that the value of a fixed-point number can be altered by moving the point.  The decimal numbers 54321, 5.4321, and 5432.1 are all quantitatively different, although in every case the component digits and their ordering are identical.  Moving the indicator point n positions to the right or left, respectively, increases or decreases the value of a number by a factor equal to the radix of the system raised to the power of n.  When fixed-point numbers are used in scientific computations, the programmer must devote considerable attention to the scaling (i.e., the radix point positions) of his numbers and to the avoidance of overflow.  The use of floating-point numbers in such computations allows the computer to handle scaling automatically and greatly reduces the problem of overflow.

In floating-point form, a number is expressed in terms of two other numbers, known as the mantissa and the exponent.  The mantissa is composed of the sign of the fixed-point equivalent, plus the same component digits with an implied indicator point to the left of the high-order digit.  The exponent is an integral power of the radix which specifies the true location of the indicator point relative to the point implied in the mantissa.  If the true indicator point is to the right of the implied point, the exponent is positive; if it is to the left of the implied point, the exponent is negative.  When the mantissa of a floating-point number is multiplied by the radix raised to the power of the exponent, the result is the equivalent fixed-point number.  Note that numbers in any positional notation system, such as decimal, binary, octal, or hexadecimal, can be expressed in floating-point form.

A few examples should help to clarify the concept of floating-point numbers:

Fixed-Point Number|Sign, Mantissa, & Exponent|Application
------------------|--------------------------|-----------
Decimal: | |
+95 | +  .95  +2 | +.95 x 10<sup>2</sup> = +95
-.030 | -  .30  -1 | -.30 x 10<sup>-1</sup> = -.030
Binary: | |
+.001 | +  .100  -2 | +.100 x 2<sup>-2</sup> = +.001
-111.000 | -  .111  +3 | -.111 x 2<sup>3</sup> = -111.000

Note that high-order zeros in the fixed-point numbers are suppressed in the floating-point representations.  This process which results in the first significant digit being immediately to the right of the point, is called _normalization_.  Normalization is discussed fully in Section XIII, in which floating-point arithmetic is explored in greater detail; the Honeywell 1800 instructions that manipulate data in floating-point form are also described in Section XIII.

## SECTION II

### THE HONEYWELL 1800 SYSTEM

#### The Equipment

A Honeywell 1800 Electronic Data Processing System consists of a central processor plus varying types and numbers of input and output units.  The programmer must know the system configuration with which he is to work.  An understanding of the function of each component and its relation to the entire system will make his task easier.

##### 1. The Central Processor (1801)

The basic central processor consists of a control unit, a control or special-register memory, an arithmetic unit, and four banks of main (or high-speed) memory, each able to store 2048 Honeywell 1800 words.  (A Honeywell 1800 word is composed of 48 information bits and six checking bits.)  To this basic unit, additional memory banks can be added in modules of 8192 words (model 1802) up to 32,768 words; further expansion is available in modules of 16,384 words (model 1802-1) up to a maximum of 65,536 words.  An optional floating-point unit (1801-B, discussed below) is also available.

The control unit with its control memory is the nerve center of the central processor.  As the site of traffic control and multiprogram control (explained below), it monitors the time sharing of the entire system to achieve maximum efficiency of operation.  In addition to its multiplexing function, it is also the unit that selects, interprets, and directs the execution of instructions, and governs address selection in both control memory and main memory.

The memory cycle time is two microseconds.  This is the time required to read one Honeywell 1800 word from memory (access) and to replace it in its original form (restoration).

The control memory is a magnetic-core array providing storage for 356 eighteen-bit words.  The read-restore cycle of the control memory is out of phase with that of the main memory in such a way that if reference must be made to the control memory between references to main memory, it is usually possible to make such reference without loss of main-memory cycle.  As discussed more fully in Section V, the control memory contains eight identical groups of special registers such as sequencing counters, index registers, registers used for indirect addressing, etc., the contents of which are used to select a full Honeywell 1800 word from the main memory.  The offset cycle of control memory makes it possible to anticipate an address selection involving the contents of a special register and to prepare the address of a second operand while another unit is using the first operand.  Because of this anticipatory technique, it is unnecessary in many cases to add memory cycles to an instruction for indexed or indirect addressing.  Even when the contents of a special register are modified before they are restored, no extra memory cycle need be added, since the special register circuitry includes a separate adder, with complete and independent checking, used only for special register modification.  This applies to both automatic modification, as when a sequencing counter is incremented after use, and program-controlled modification, as when an increment is specified in an address.  However, while the two memory units are sufficiently out of phase to allow reading from the control memory prior to the start of a main memory cycle, a read-restore operation in which the result of an instruction is returned to a special register cannot overlap a main memory cycle; in this case, an extra cycle must be added to the instruction time.

The arithmetic unit is the portion of the central processor in which digits are combined to form new arrays in accordance with the logical rules of the command codes.  The Honeywell 1800 central processor has provision for both binary and decimal arithmetic, complete logical abilities, and competent internal checking.  For the interested reader, a complete description of the fixed-point addition logic can be found in Appendix A.

##### 2. The Floating-Point Option (1801-B)

The floating-point option (1801-B) is a second control and arithmetic unit which provides the Honeywell 1800 user with 19 instructions that manipulate data in floating-point form, plus two fixed-point division instructions.  The control portion of the unit selects, interprets, and directs the execution of these instructions by the arithmetic portion.  In an 1800 system not equipped with an 1801-B, these instructions are not executed directly but are interpreted as pseudo instructions which call in library routines to perform the desired operations.  Descriptions of this unit, its component registers, and the instructions it provides are presented in Section XIII.

##### 3. The Console

The Honeywell 1800 console is basically a part of the central processor and is multiplexed into the system via multiprogram control (see below).  A monitor typewriter is used by the operator to communicate directly with the central processor.  Manual operations on the typewriter can start and stop individual programs and interrogate Honeywell 1800 storage.  Under program control, the console typewriter can also print information useful to the operator.  An additional typewriter, called the console slave typewriter, can be added to the system.  No manual operations can be performed from the slave typewriter, but printing can be programmed to occur on either the slave or the console monitor typewriter.  In addition to the typewriter(s), the console includes display lights that give the operator an at-a-glance summary of the number of active programs, their control centers, and their progress.  The console also includes a modular display panel which has indicators and displays for monitoring the status of tape units and other peripheral devices.

##### 4. Magnetic Tape Units (804) and Tape Controls (803)

The Honeywell 1800 magnetic tape units are designed for reliability and accuracy.  The recording surface of the tape is untouched except by the read/record head, insuring that wear and damage to the the surface are held to an absolute minimum.  Vacuum is used to seat the reels on the hubs, to maintain loops in the loop chambers, and to provide contact with the capstans which cause the tape to move under the head, giving accurate control without the dangers inherent in mechanical techniques.  The tape is edge guided along its entire path to protect the tape from damage and to avoid skew.

The system uses 3/4-inch-wide tape with Mylar [1] (polyester film) base and oxide coating.  The recording portion of a full reel of magnetic tape is 2500 feet in length, ± 50 feet.  A 30-foot clear leader precedes the recording portion and a 25-foot clear leader follows it.  Information is written on tape in 10 longitudinal channels, eight for information bits from the word, one for a parity-checking bit, and one for a clocking indicator.  One array of bits across the tape is called a frame.  Information from six frames makes up the 54-bit word, which includes six parity bits.  The clocking channel gives positive indication of the frame location on tape.

[1] Mylar is a registered trademark of E. I. du Pont de Nemours and Co., (Inc.).

Variable-length recording is a basic feature of the Honeywell 1800, and records of any size may be read from or written to on tape, although for control purposes a maximum size limit may be placed on records at the beginning or end of tape.  Gaps between records are 0.67 inch long.

Three different tape units are available for the Honeywell 1800.  Their recording and rewind speeds, recording densities, and transfer rates are shown in the table below.  All three tape systems are compatible: data recorded by one system can be read at recording density by the others.

```
Model                                  Speed         Recording Density   Transfer Rate
                                (inches per second)  (frames per inch)   (decimal digits per second)

                                Read/Write  Rewind

804-1 Magnetic Tape Unit            120      360            400              96,000
804-2 High-Density Magnetic         120      360            555.5           133,300
      Tape Unit
804-3 Economy Magnetic Tape Unit     60      180            400              48,000
```

When rewinding, the tape moves at three times normal speed.  A small photo-electric device in the tape unit senses the presence of edge "windows" (clear Mylar) in the tape to provide beginning-of-tape and end-of-tape indications for the programmer.  A physical slot in each leader is sued to negate the vacuum and stop the unit when the end of tape is reached.

When a metal ring is inserted in the front of a tape reel, writing is allowed to take place on the tape.  When this ring is removed, the tape is protected and cannot be written upon.  The ring may be installed or removed without rewinding the tape or removing the reel.  There is, in addition, a manual switch on the tape unit panel which can be set to prohibit writing.

A tape control can control up to eight tape units.  The model 803-1, 803-2, and 803-3 tape controls are used with 804-1, 804-2, and 804-3 tape units, respectively.  Each control uses an input and an output channel so that one of the tape units attached to the control may be reading and another writing simultaneously.  Designation of tape units as active or inactive is accomplished through the use of the tape address patchboard on the maintenance and indicator panel of the tape control.  The patchboard also allows for the re-addressing of tape units; for example, the unit physically designated as number 1 may have, as a result if patchboard plugging, an effective address of 3.

##### 5. The Card Equipment

###### a. Card Readers (823)

Two 80-column card readers are available with the Honeywell 1800 System.  From the programmer's point of view, these two readers differ only in that the 823-1 reads 240 cards per minute and the 823-2 reads 650 cards per minute.  In the manner in which they respond to instructions and transmit information, they are identical.  Either may be used on-line (connected to the control processor via a card reader control) or off-line (connected to a tape unit via a card reader control and an off-line auxiliary control, see below).

In on-line operation, the card reader with its control reads the card, converts the punch configuration to Honeywell 1800 notation, and transmits the information to the main memory.  By means of a 3-position switch, the operator selects the mode of conversion - alphanumeric (normal) or transcription.  If the alphanumeric mode is used, card conversion results in the transmission of 10 Honeywell 1800 words of eight characters each, where the high-order character of the first word corresponds to column 1 of the card and each successive 6-bit character in the next lower-order position corresponds to the next higher-numbered column.  In one position (FULL), the switch defines as legal the entire 64-code set listed in Table 1, page 167, which shows the correspondence between punched-card codes and Honeywell 1800 codes; in a second position (STANDARD), the legally defined set is 50 characters, excluding the asterisked codes in Table 1.

A third switch position (TRANSCRIBE) allows the processing of information punched in transcription mode, in which the information from each card read is transmitted to the main memory in 20 Honeywell 1800 words.  The value of each of the 960 bits indicates the presence or absence of a punch in a specific punching position.  Figure II-1 shows the correspondence between card format and memory format in both the alphanumeric and transcription modes.

Each of the card readers has tow reading stations.  The results of the two readings of each card are compared, and any discrepancy is noted.  As the 80 columns of information are converted in the control, additional checking is done to insure correct conversion.

One extra word is appended to each card record as it is sent to memory, indicating the status of the error indicators at the completion of the reading and conversion operation for that card.  Thus, a standard card record is either 11 words (alphanumeric mode) or 21 words (transcription mode).  When cards are read on-line, the control word is composed entirely of zero bits with the exception of bits 15 and 16, which are used to indicate:

!(images/figure_II-1.png)

1.  That the card was punched, read, and converted correctly (11 in bits 15-16);

2. That the card contained a punch combination defined as illegal but was read and converted correctly (01 in bits 15-16);

3. That an error occurred during reading or conversion (10 in bits 15-16).

Note:  In the event that an illegal punch coincides with an incorrect read or conversion, the latter signal takes precedence (i.e., bits 15-16 are 10).

###### b. Card Punch (824-1)

The 824-1 punches 100 cards per minute, operating either on-line or off-line.  the card punch is capable of punching in the same two modes 
in which the card readers can operate, and the relationship between the card format and the format of information within the Honeywell 800 is identical (see see Figure II-1).  The selection of the mode to be used in punching an individual card, however, is made by the program.  A control word _precedes_ the actual information to be punched, sets the punch to accept either 10 or 20 information words, and informs the punch control as to which conversion mode is desired.  Only four bits of the control word are used by the punch control.  The values of bits 16 and 17 specify the desired conversion mode and hence the number of words to be accepted.  If the control word contains zeros in both bit 16 and bit 17, the alphanumeric mode is used; if these bit positions are both ones, the transcription mode is used.  A zero-one or one-zero combination is illegal, and can cause the punch to enter either mode.  Ones in bit positions 13 and 14 cause the punch to stop with an indicator lit, signifying that the punching of a file is completed.  The control word is coded identically for both on-line and off-line operation.

###### c. Card Reader - Card Punch (827-1)

The card reader - card punch, model 827-1, reads 800 cards per minute and punches 250 cards per minute.  Otherwise, it has all of the properties of the card readers and punch described above, including the capability for either on-line or off-line operation.  The 827-1 requires separate peripheral controls (or a single model 811 multiple terminal control unit, see page 21) to handle the reader and punch sections.  This unit is capable of simultaneous reading and punching, except when connected to a multiple terminal unit control.

##### 6. The Printers (822)

###### a. Standard-Speed Printers

The standard-speed printers, models 822-1 and 822-2, are 407 and 408 tabulating machines, printing 150 lines per minute.  Both printers can operate either on-line or off-line.  Ten characters are printed to the inch over a spread of 12 inches, providing a total of 120 characters per line.  Vertical spacing is six or eight lines to the inch.  Forty-seven different characters are available: 26 alphabetic, 10 numeric, and 11 special symbols.

A 12-channel, punched paper carriage tape is used for vertical format control.  In on-line operation, the central processor transmits a control word (containing vertical format information) and 15 information words to the printer control.  The information words are treated as 120 alphanumeric characters, with the high-order character of word one corresponding to the leftmost printing position.  The vertical format control word contains two 6-bit characters (bits 19-30) which correspond to the 12 channels of the carriage tape.  A one in any of these bit positions designates a controlling carriage-tape channel, and the carriage is advanced until the next punch is sensed in the designated channel.  By means of plugboard wiring, these 12 bits may be used to effect most of the normal plugboard controls, such as single or double spacing, suppressed spacing, extra spacing, overflow, non-print, skip, head of form, etc.  In addition, ones in bits 13 and 14 of the control word cause the printer to stop with an indicator lit, signifying that the printing run is completed.  The coding of the control word is identical for both on-line and off-line operation.  Values of bit positions other than those specified are ignored.

The tabulators retain most of the abilities normally provided through plugboard wiring.  In parituclar, the comparison abilities of the 408 are retained.  The 822-2 (bill-feed printer) can print on cut forms as well as on continuous forms.

###### b. High-Speed Printer

The high-speed printer, model 822-3, has a rated speed of 900 lines per minute for continuous single-space printing and approximately 800 lines per minute for continuous double-space printing.  Printing can be accomplished either on-line or off-line.  There are 160 print positions of which any prescribed array of up to 120 can be activated during a run.  At each print position, a total of 56 characters is available: 26 alphabetic, 10 numeric, and 20 special symbols in either standard or selfchek #12F font.

Horizontal spacing is 10 characters to the inch. Vertical spacing is six lines to the inch; a special option allows the selection of either six or eight lines to the inch by means of a switch.  Skipping speed in the non-printing mode is approximately 20 inches per second.  Vertical format is specified by a control word in conjunction with a pre-punched, 6-channel, paper carriage tape.  Both horizontal and vertical vernier adjustment of form position are standard.

For each printed line, 16 words are sent to the printer control.  The first word contains vertical-format information, and the remaining 15 are interpreted as 120 characters to be printed.  The high-order character in the first information word corresponds to the first line of the 120 print positions selected to be active.  Line spacing is directed by the vertical-format word as follows:

    Bit  1      Position at head of form, as indicated by a punch in 
                channel 4 of the carriage tape, if bit 1 is a one.

    Bit  6      Inspect channel 3 of the carriage tape for punch 
                indicating end of form.

                If bit 6 is a one, the macine senses for end of form as determined by a punch in channel 3 of the paper tape.  When the punch is sensed, the carriage is advanced to the beginning of form.  Normally, in a listing, bit 6 always has the value of one, so that the end-of-form channel is continually examined.

    Bits 7-12   Advance paper the number of lines (0-63) indicated by 
                the contents of bits 7-12 after the accompanying line has been printed.

    Bits 13-14  Stop for end of run.  If bits 13 and 14 are ones, the 
                printer stops with the END RUN light glowing to signal that the run is complete.

Values of bit positions other than those described above are ignored, making it possible to edit a record for listing on either a standard-speed or high-speed printer.  The coding of the control word is identical for both on-line and off-line operation.

##### 7. The Paper Tape Equipment

###### a.  Paper Tape Reader and Control (809)

The model 809 paper tape reader and control operates on-line in the Honeywell 1800 System, reading punched paper tape into the central processor.  The input tape must be chadded (clean hole), opaque, non-oiled, and non-metallic, although a special option permits the use of metallic paper tape.  Three sizes of tape can be used with the reader:  11/16 inch, five-channel tape; 7/8 inch, six- or seven-channel tape; and one-inch, eight-channel tape.  The tape may be read under reel-servo control or as strip segments.  Two reel sizes are available: 5-1/2 inch reels which store 350 feet of tape, and seven-inch reels which store 700 feet, plus four feet of leader at each end.

Each read forward instruction causes one frame (character) to be read from paper tape into main memory.  Under reel-servo control, a nominal tape reading speed of either 500 frames (50 inches) or 1000 frames (100 inches) per second may be selected by means of a switch; strip segments are always read at 500 frames per second.  Rewind speed is either 50 or 100 inches per second, depending on the reading speed selected, and the tape can be wound onto either the supply reel or the takeup reel.  During reading, frame punches are converted and stored as the low-order bits of a main memory location, with zeros supplied as high-order fill.  If the tape has parity punches, the control checks frame parity; it can be set to handle either odd or even parity.

The logical end of tape is normally indicated by the presence of adhesive-backed pieces of metal foil.  When the foil is not used, the end of tape may be detected by the presence of a particular punch pattern, by the absence of sprocket holes, or by the loss of tape tension.

###### b. Paper Tape Punches and Controls (810)

The models 810-1 and 810-2 paper tape punches and controls operate on-line with the 1801 central processor.  Both models combine a control unit with a punch which punches ten frames to the inch at a speed of 110 frames per second.

The 810-1 handles 11/16 inch paper tape and punches 5-level code; the 810-2 can handle either 7/8 inch tape for punching up to seven levels, or 1-inch tape for punching up to eight levels.  The punches will accommodate most kinds of commercially available paper tape, in reels of up to 1200 feet.  Oiled tape is recommended for use wherever possible.  Metallic paper tape can not be used.  The punches produce one frame of chadded (clean hole) paper tape in response to each write instruction from the central processor.

All bits of the frame to be punched, including parity bits (if any), must be stored in the main memory as the low-order bits of a word.  Tape movement is anticipatory; after a frame has been punched, the tape is advanced one frame length in anticipation of the next write instruction.  Bit 40 is used to signal end of run; unused bits from bit 333 to the first information bit must be zero-filled.  The high-order 32 bits are not sensed and their values are irrelevant.

A standard parity check is sued to verify the correct transfer of information from main memory to the punch control.  The amount of tape on the supply and takeup reels is sensed by detectors which signal the central processor when the supply of tape drops below approximately 20 feet or the takeup reel becomes full.

##### 8. Off-Line Controls (815, 816, 817, and 818)

When a terminal unit is used with a magnetic tape unit independently of the central processor, as in a card-to-tape or tape-to-printer operation, an off-line auxiliary control is placed between the peripheral control and the tape unit to provide control signals and power normally supplied by the central processor.  If the terminal unit is a card reader, then an off-line input auxiliary control (816) must be used.  In like manner, a printer or card punch requires an off-line output auxiliary control (815) and a multiple terminal unit control (see "System Configurations," below) calls for an off-line input/output auxiliary control (817).

For off-line printing or card punching, information is read from magnetic tape into the auxiliary control and stored frame-by-frame in the memory of the peripheral control.  Reading occurs only in the forward direction of tape travel.  When the peripheral control has received and stored the number of words required to process a record, it ceases to accept information.  To accomplish the desired printing or punching tape tape records should be organized in the following manner:
1. For printing, each record should contain one control word, 15 information words, and two orthotronic control words, in that order.
2. For alphanumeric mode card punching, each record should contain one control word, 10 information words, and two orthotronic control words, in that order.
3. For transcription mode card punching, each record should contain one control word, 20 information words, and two orthotronic control words, in that order.
4. The control word of the last record on a tape should contain an end-of-run code.

The end-of-record word generally appearing at the end of each tape record is not sensed in the off-line auxiliary control, which instead senses the interrecord gap and signals the magnetic tape unit to stop the tape.  When the record has been correctly printed or punched, the next tape record is read into peripheral memory.

An alternative off-line printing configuration is available, using the model 818 off-line printer control to connect a high-speed printer and a magnetic tape unit.  Thus, the 818 performs the functions of both the peripheral control and the off-line auxiliary control.  In this configuration, unlike the use of an off-line auxiliary control, the printer is not available for on-line printing.

When reading cards off-line, each card is read, converted, and checked in the same manner as on-line reading, then written on tape as a record.  In alphanumeric mode, each record consists of 10 information words, one control word, two orthotronic control words, and one end-of-record word, in that order. In transcription mode, each record consists of 20 information words, one control word, two orthotronic control words, and one end-of-record word, in that order. 
The two orthotronic control words and the end-of-record word are automatically generated by the off-line auxiliary control.

##### 9. Additional Equipment Available in the Honeywell 1800 System

###### a. Random Access Storage and Control (860)

The 860 series random access storage files and controls provide large-capacity auxiliary storage in the form of magnetic discs.  Each disc stores 524,288 words or 6,291,456 decimal digits.  The number of discs in a random access storage file ranges from twelve in model 860-1 to 192 in model 860-9.

###### b. Optical Scanning Unit and Control (840)

The model 840 optical scanning system enables documents printed in Selfchek #12F font by the high-speed printer to be used as on-line input to the 801 central processor.  Honeywell has also developed an Orthoscanner, a device which optically reads pre-printed bar codes.

###### c. Communications Control (880)

The 880 communications control allows the 1801 central processor to receive and transmit data over toll or leased-wire circuits.  With a communications control as part of the equipment complement, an 1800 system can communicate with a similarly equipped Honeywell system, and with a number of other systems.  At any given instant, the communications control can either transmit or receive information.

###### d. Tape Control (836)

The model 836 tape control transmits data between an IBM type 729 II tape transport and the 1801 central processor.

###### e. Magnetic Tape Switching Unit (805)

The model 805 magnetic tape switching unit is used to switch control of one 804 magnetic tape unit from one to the other of two controls, which can be any combination of the following: 803 magnetic tape control, 815 off-line output auxiliary control, 816 off-line input auxiliary control, 817 off-line input/output auxiliary control, and 818 off-line printer control.

###### f. Real Time Control Units (812)

For real time operations Honeywell real time control units provide buffer storage and associated control equipment for buffering information into and out of the 1801 central processor, plus a specified interface to which external real time equipment may be designed.  The model 812-1 control is an on-line device which transmits and accepts data non-simultaneously.  The model 812-2 control, also an on-line device, transmits and accepts data simultaneously.

###### g. Programmed Elapsed Time Clock (1813-3)

The model 1813-3 elapsed time clock is connected to the 1801 central processor via either a peripheral input or output trunk.  It stores a count of time, in seconds and sixtieths of a second, during which the central processor is in operation.

###### h. Programmed Real Time Clock (1813-4)

The 1813-4 real time clock is used to supply time-of-day information, in hours, minutes, and seconds, to the central processor and to a visual display.

###### i. Honeywell 1800 III

An H-1800 III system consists of an 1801 central processor and its normally associated peripheral devices, augmented by an H-200 computer which is directly connected via a model 212 on-line adapter.  The adapter provides all of the buffer and indicator facilities necessary to allow any of a possible eight programs running in the larger system to control a program running in the H-200 and to initiate memory-to-memory data transfers between the two systems.  Typically, the facilities provided by the 212 adapter are used to allow an H-1800 program to initiate and control: 1) simple input/output operations involving reading or writing by H-200 peripheral equipment and memory-to-memory data transfers; and 2) semi-independent "macro" operations such as card-to-tape, tape-to-printer, and tape-to-card media conversions which are running in the H-200.  Programming considerations for the H-1800 III are presented in the bulletin "Model 212 On-Line Adapter" (DSI-274).

#### Traffic Control

Traffic control is the Honeywell 1800 element which directs the time-sharing of memory by the tape and peripheral units and the central processor.  Peripheral buffer control is the element which reconciles the 6-microsecond buffer cycle of a peripheral control to the 2-microsecond H-1800 memory cycle.  Multiprogram control is the element which directs the time-sharing of the central processor by the active program control centers.  A clear concept of these elements is basic to the understanding of parallel processing and allowable system configurations and is the key to a thorough knowledge of the Honeywell 1800.

Traffic control has as its main object the efficient use of the entire system according to a set of priorities which derive directly from the nature of the equipment and are independent of the programs.  For example, an 804-1 magnetic tape unit reading at full speed assembles one Honeywell 1800 word in a one-word buffer every 125 microseconds.   If instant access is not provided to memory, a second word of buffer storage must be provided to retain this word.  At the end of the next 125 microseconds, another word will have been read.  If the first word has not yet been placed in main memory, another word of buffer storage must be provided.  Since eventually one access to memory must be made for each word to be stored, it is obviously economic to store each word as it is assembled from tape and thus reduce the required buffer storage to a minimum.  However, to keep the memory continuously available to the tape buffer during a read operation would be to introduce inefficiencies in the system, for only one memory cycle (two microseconds) is needed to store each word, and during the remaining 123 microseconds the entire system would be idle.

In the Honeywell 1800, one access to memory every 125 microseconds is guaranteed each tape unit.  When a word is assembled from six frames for storage, a demand signal is generated by the buffer for one access to memory and is honored within 125 microseconds, clearing the buffer.  In this case, only two words of storage are needed for each active tape unit, and the memory is utilized by the input/output operation only 2n microseconds out of each 125 microseconds, where n equals the number of active units.  To achieve this time-sharing, traffic control monitors the demand signals from the buffers and arranges access to the memory within the prescribed time for each buffer demand.

The peripheral buffer control is an interface which makes the 6-microsecond buffer cycle of the peripheral controls compatible with the 2-microsecond memory cycle of the Honeywell 1800.  Specifically, six microseconds are required to effect a 1-word transfer between the peripheral buffer control and a standard peripheral control unit.  Only two microseconds, however, are required to transfer one word between the main memory and the peripheral buffer control.  The two microseconds of main memory transfer are overlapped with the first two of the six microseconds needed for the transfer to the peripheral control unit.

As its name implies, traffic control monitors the transmission of information to and from main memory.  Its operation is represented schematically in Figure II-2.  The 17 divisions of the band are called "stages" and one stage is assigned to each of the eight output channels, each of the eight input channels, and the central processor.

!(images/figure_II-2.png)

The creation of a demand signal by any device is represented in Figure II-2 by the closing of the switch shown in the corresponding control stage.  When any program has been turned on in the central processor, the switch corresponding to the central processor stage is continually closed.  Traffic control begins each scan at the left end of the band.  It proceeds to the right, ignoring all stages which show no demand signal, until a demand stage is reached.  This stage is allowed access to the main memory for one memory cycle only.  Traffic control then returns to the left end of the band to begin the next scan.  Because the control search is anticipatory, no system time is consumed in bypassing stages in which no demand exists.

If no input/output devices are active but a program is running, the central processor stage will have complete use of the memory since each scan of the band will find no other demand signals.  If a magnetic tape unit attached to channel 1 is reading, then once every 125 microseconds a demand signal will halt traffic control at the stage marked "input 9" for one memory cycle to allow transfer of the assembled word from buffer storage to memory.  Should all 16 input/output stages issue demands simultaneously, a total of 96 microseconds (16 times 6) would elapse before all demands were satisfied, but the central processor would only be interrupted for 32 (16 times 2) microseconds.

Since, in normal read-write operations, only one buffer cycle may be allowed any stage before the next scan of the band, a maximum of 16 buffer cycles or 96 microseconds will elapse between successive interrogations of any stage.  As this is within the 125 microsecond maximum, eight 804-1 tape units may be reading and eight may be writing simultaneously with central processor operations without conflict in demands for access to memory.  Furthermore, since the memory is made available to the central processor for any cycle in which it cannot be utilized by an input/output stage, no idle time is introduced as long as any program is active.  Thus, traffic control insures that the system responds to input/output device demands as required without introducing idle memory cycles, adn that as long as any program can proceed, useful work is being done.

The rule of operation which states that only one buffer cycle may be allowed any stage before the next scan has one exception.  When a magnetic tape unit is executing a distributed read or distributed write operation, two consecutive buffer cycles are allowed a stage for modifying the appropriate address counter on recognition of the demand signal accompanying and end-of-item word.  Distributed read and write instructions are more fully discussed in Section XL.  Two points in connection with with this exception bear mentioning here.  First, the difference between the normal 96-microsecond cycle and the maximum allowable 125-microsecond cycle allows servicing of four such demands without timing conflicts.  Secondly, in the improbable case that all system channels are active and five or more channels are being used in distributed tape operations, and at least five of these each assemble an end-of-item word and create a demand signal within 125 microseconds of each other, an error signal will be generated for any unit whose demand is not serviced within the required time limit.  This signal will appear to the program as a normal reading error signal indicating the need for a reread from the specified unit.  Complete information is available to the program so that intelligent action can be taken under program control.

The preceding discussion of traffic control is based on the use of model 804-1 magnetic tape units which have an instantaneous transfer rate of 96,000 decimal digits per second.  The use of input/output units with higher transfer rates may not permit simultaneous use of all 16 input/output channels.  For example, the model 804-2 magnetic tape unit, with an instantaneous transfer rate of 133,300 decimal digits per second, requires one access to memory every 90 microseconds when operating at full speed.

All existing 1800 peripheral devices have 6-microsecond buffer cycles and are designed to be attached to peripheral buffer control.  However, it is possible to attach special high-speed devices having 2-microsecond buffer cycles directly to traffic control.  It is also possible, by means of a simple field change, to modify the traffic control priority of any input/output trunk(s) within the following restriction: a 6-microsecond read priority cannot be rewired to interrupt a sequence of 6-microsecond write priorities.

#### System Configurations

The central processor is the heart of any Honeywell 1800 installation.  Peripheral devices and magnetic tape units are attached to the eight input and output channels of the central processor.  Input and output channels alike are numbered 1, 2, 3, 4, 5, 6, 7, and 0.  The output channels are associated with stages 1-8 of traffic control; the input channels are associated with stages 9-16.  Each channel has a priority according to the sequence in which the corresponding stage of traffic control is interrogated.  In other words, output channel 1 has the highest priority, and input channel 0 the lowest.  Each special register group includes an input buffer counter and an output buffer counter associated, respectively, with an input and an output channel.  Thus output and input channels 1 are associated with the buffer counters of special register group 1, while output and input channels 0 are associated with the buffer counters of special register group 0.  There exists no relationship between the special register group whose buffer counters are associated with a particular device and the special register group controlling the program which uses that device.

Any device requiring both an input and an output channel for simultaneous use, such as a tape control, must be assigned to channels whose associated buffer counters reside in the same special register group.  Otherwise, any input device may be assigned to any input channel and any output device to any output channel, subject only to the restriction that tape controls must be assigned to channels of higher priority than peripheral controls.  Specifically, if an installation includes two tape controls, a card reader, and two printers, the first tape control is assigned to output and input channels 1 and the second tape control to output and input channels 2.  The card reader may be assigned to any remaining input channel and the printers to any remaining output channels.

Each tape control may control up to eight magnetic tape units.  The tape units connected to a tape control are normally assigned consecutive positions starting with position 1.  However, since tape addresses are assignable by patchboard, the programmer will find this no restriction.

In most systems each terminal unit will have its own control.  The exception is the use of a model 811 multiple terminal unit control to control a card reader, a card punch, and a printer (or any two of these devices).  The multiple control unit has a single buffer which can handle traffic in either direction.  Thus, only *one* device, either input or output, may be used at a time.  Selection of the device to be used is made by a manual switch on the multiple terminal unit control.  If the multiple control unit has both a card reader and an output device attached, it must be assigned both an input and an output channel.  Since only one device may be used at a time, however, the channels assigned need not be a corresponding pair.

#### Multiprogram Control

Multiprogram control directs the time-sharing of the central processor by the active programs.  Each of the eight groups of special registers may direct the execution of an independent program.  After a program is loaded, one of the special register groups is activated to direct the selection of instructions.  This special register group, and the program it directs, is said to be "on."  When the program is completed, the directing special register group is inactivated (turned "off").  Special register groups may be turned on and off independently of each other, either from the console or by program control.

Each time traffic control allows the central processor access to main memory, one memory cycle of one instruction is performed.  If only one special register group is active, all cycles allowed the central processor are used in executing instructions from the active program.  Since traffic control allows the central processor all available cycles except those needed to honor the intermittent demands of tape and peripheral devices, this case represents that of the conventional single-program computing machine with the ability to implement input/output operations simultaneously with computing.

When more than one special register group becomes active, central processor cycles must be shared among the several programs.  The rules under which multiprogram control operates are as follows:

1. When an active special register group is selected, the next cycle allowed the central processor must be used to select the next instruction to be executed in the program controlled by that group.
2. All succeeding central processor cycles must be devoted to the execution of this instruction until it is completed.  (This may range from two cycles upward.)
3. If the instruction is one which does not leave unstored information in the arithmetic or control units, its completion causes multiprogram control to scan or "hunt" for the next active special register group in sequence.
4. If the instruction does leave unstored information in the arithmetic or control unit, scanning or hunting is inhibited and the next instruction is selected from the same program.  Hunting is not allowed if:
   a. the instruction generates a two-word result, of which only one word is stored in memory as the result of the instruction execution, e.g., multiply;
   b. the execution of the instruction results in a sequence change; in the case of a conditional change, hunting is inhibited only if the condition is satisfied;
   c. the instruction has an inactive C address;
   d. an unprogrammed transfer takes place as the result of executing the instruction;
   e. the instruction is capable of specifying that hunting shall not take place, and does so specify.

For example, if three programs are active, then one instruction is performed in turn from program 1, then 2, then 3, then 1, and so on, as long as all instructions selected allow hunting.  Such alternation is *temporarily* held up if an instruction is selected which does not allow hunting, but it is resumed as soon as an instruction is selected which does allow hunting.  Thus, the central processor cycles are shared on a fairly equal basis among all active programs.

The true power of multiprogram control appears when an active program attempts to execute an instruction which cannot be implemented because of the unavailability of a system component.  Suppose, for example, that a write instruction calling for tape 4 is selected from an active program.  The central processor, in attempting to execute this instruction, finds that either tape 4 or its associated output channel is involved in executing another instruction from the same or some other program.  Seeing that the instruction cannot be executed immediately and recognizing the reason therefore, multiprogram control places the special register group in a "stall" condition.  This condition indicates to multiprogram control that a) this program, although still active, shall not be allowed any central processor cycles as long as the "stall" indication remains, and b) when the channel and/or the device involved completes its present task, the stall condition shall be automatically removed and the program restored to its full active status.

Thus, when an instruction cannot proceed because of input/output conflicts with either the same or another program, the central processor cycles which it would have used are made available to the other active programs, causing them to proceed faster.  The result of the operation of multiprogram control is that there is never an idle memory cycle in a Honeywell 1800 system as long as there is any active program in which an instruction can be executed.

If more than one active program is stalled because of input/output conflict, multiprogram control remembers which program was stalled first and operates on a "first off - first on" basis.  Other stalled programs are activated according to the normal scanning sequence.

Although it need not concern the programmer, the reader may be interested in a short discussion of the actual machine procedure in case of program "stalls."  The computer will have selected the instruction and entered the second cycle of execution before the unavailability of the input or output channel and/or device is discovered.  No memory alteration will have been made, but the sequencing counter will have been advanced by one.  When the stall condition is ascertained, the computer will subtract one from the sequencing counter and deactivate the program from multiprogram control.  Each time that any input/output channel or device terminates an operation, all programs in a stalled condition are reactivated.  Multiprogram control looks again at each reactivated program, replacing in a stalled condition those programs whose input/output demands still conflict.

Multiprogram control also receives demand signals generated by the console and by inquiry stations.  The console is regarded by multiprogram control as a ninth group of special registers, except that it takes precedence over any active program in the assignment of available central processor time.  A demand signal from the console is serviced at the time of the next hunt, although a non-hunting sequence of instructions will not be interrupted.

When a console demand is recognized, the computer generates an instruction to implement the activity indicated by the console command.  Sufficient memory cycles are then assigned to execute this generated instruction in the same fashion as if it had been selected from memory.  When the instruction has been executed, the normal hunting process is resumed.  If the system includes one or more remote inquiry stations, demand signals from these stations are recognized and implemented in a similar fashion.  This technique allows the operator to communicate manually with the central processor without stopping the computer, and thus allows the system full-efficiency operation even during manual manipulation on one program.

#### Orthotronic Control and Checking

Orthotronic control is a powerful technique, exclusive with Honeywell, which insures against loss of information from magnetic tape during writing, storage, or subsequent reading.  Experienced data processing personnel know that long storage periods or inept operator handling can cause information to disappear from a tape even though the accuracy of the record was checked at the time the record was written.  Even infrequent occurrences of this type can result in many man-hours and machine-hours spent in re-creation of the records.  While no technique will every completely eliminate information loss, the high reliability and accuracy of the Honeywell 804 tape units, plus the presence of orthotronic control as a standard feature of every Honeywell 1800 system, insure that such loss is eliminated as a practical problem.

Orthotronic control is based on studies of the types and extent of information losses which have occurred on magnetic tape systems.  It is partly automatic and partly program-controlled.  An instruction is provided which automatically creates two orthotronic words for a specified record.  These words a re a logical combination of all the words in the record such that only a highly unlikely periodicity of error can go undetected and uncorrected.  The orthotronic words are automatically positioned to accompany the record as it is written.  Read and write instructions assume the presence of the orthowords and automatically include them in the record, using them in an automatic first-level check of the correctness of the information handled.  The instruction which generates the original orthowords may also be used to reconstruct missing information if loss is detected.  A full discussion of orthotronic control can be found in Appendix B.

Orthotronic control is a checking device peculiar to the magnetic tape units.  In on-line operation, the central processor must be programmed to reconstruct lost data from a garbled record.  When tapes are read or written in an off-line configuration, however, an off-line auxiliary control provides, in part, the central processor function.  The off-line input auxiliary control automatically generates the two orthowords which must accompany each record when it is read by the central processor, and performs the first-level check on the information which involves these two words. The off-line output auxiliary control performs a check of every record read exactly as the central processor does, and is capable not only of detecting an error in the record but, in the majority of cases, of reconstructing the garbled information.  The corrected information can then be printed or punched without stopping or repositioning the output device as would be necessary without such automatic error correction.

In addition to orthotronic control, and in some ways complementing it, a parity bit is written on tape accompanying each frame.  The parity bit is read from tape together with the eight information bits of the frame and remains with these bits as frames are collected to form words.  As each word of six frames is transmitted to memory, the accompanying parity bits are monitored to insure an error-free transmission.  Each time a word is sent to or from main memory, a transmission check is performed using these six parity bits, and when the word is again written on tape, each bit accompanies its corresponding frame.

When a word is brought to the arithmetic unit, the computer generates a modulo-3 check on each frame pair (16 information bits) for use in checking arithmetic operations.  The value of the 2-bit mod-3 check digit is the remainder (a value from 0 to 3, where either 0 or 3 may represent no remainder) which results when the decimal equivalent of the 16 bits is divided by 3.  After the mod-3 check is generated, the parity bits are checked and then replaced by the six mod-3 checking bits.  When arithmetic operations have been completed and the mod-3 check has been performed to insure that they have been completed correctly, the parity bits are again generated, replacing the mod-3 bits.

The control unit of the central processor checks the interpretation and execution of the program instructions.  Selection of instructions and operand locations is checked.  The checking process of an add instruction illustrates the thoroughness of the Honeywell 1800 checking system.

1. The selection of the instruction location is verified.
2. The instruction itself is verified for proper parity.
3. During the processing of the A address:
   a. a mod-3 check group is attached to the address, then independently recalculated and compared with the original when this information is transferred to the memory selection circuits;
   b. the selection operation is verified by comparing with the mod-3 check for the original address the special check digits delivered with the operand;
   c. the operand itself is checked for proper parity when read from memory;
   d. three mod-3 check digits associated with the operand are generated and stored.
4. During the processing of the B address (when the contents of the B address are added to those of the A address), steps a, b, and c are repeated for the B address.  Also, three mod-3 check digits are generated as in 3d, but are added (mod-3) to the check digits previously stored.
5. As the result of the addition is transferred to memory, the C address memory selection is verified as in 3a, b, and c, and a new set of mod-3 check digits is formed from the computed sum and compared for equality with the check digits sum formed in (4) above.  If the two sets of digits are equal, then the add instruction has been processed properly.
6. An example of the mod-3 arithmetic follows:
```
Number in A address                         8426      9721      4075
The associated mod-3 check digits             2         1         1
Number in B address                         1276      0216      4925
The mod-3 check digits                        1         0         2
The sum of A and B is                       9702      9937      9000
The mod-3 check digits                        0         1         0
The mod-3 sum of the check digits is          0         1         0
```
In the general case where carries might occur between the operand groups, corrections of +1 and +2 are added to the appropriate check digits.  Since two groups are simultaneously affected by a carry correction, any error in the addition, including the carry generation or correction process, is automatically detected.

Each of the special registers retains a mod-3 check on the 16 information bits it contains, which is used to check transmissions and arithmetic operations within the control unit.  When the contents of a special register are transferred to the arithmetic unit or to main memory, they are expanded to full-word form and the mod-3 check is replaced by parity bits.

Card reading is checked not only for correct reading by the equipment, but, in the alphanumeric mode, for correctness of conversion and proper keypunching also.  Card punching is checked on the 824-1 punch for double-punched and blank columns.  Thirty columns of double-punch, blank-column detection are provided in the standard-speed punch; 80 columns are provided in the high-speed punch.  The punch section of the 827-1 reads each punched card and checks it contents against the punch image.  Printing is also checked by comparing echo pulses generated by the printer against the print image.

## SECTION III

### THE HONEYWELL 1800 WORD

The basic unit of information in the Honeywell 1800 System is a fixed-length word consisting of 54 binary digits, of which six are parity bits used by the automatic checking circuitry and 48 are information bits.  Each main memory location is capable of storing one such word, and each arithmetic register is one word in length.  A main memory word may represent a machine instruction or one or more pieces of data.  In addition to the main memory, the central processor includes the control memory of 256 special registers, used primarily for control purposes and address modification.  A special register has the capacity to store a partial word consisting of 16 information bits and two checking bits.  The extension of the special register word to 24 bits to handle memory capacities in excess of 32,768 words is described in Appendix F.

The check bits of the main memory and special register words are not directly available to the programmer, nor are their values subject to program control.  Subsequent discussions of the Honeywell 1800 word, therefore, will refer only to the information bits, unless otherwise noted.

#### Data Words

A computer program generally manipulates data in one or more different forms: decimal, alphanumeric, binary, or a combination of these.  The Honeywell 1800 is capable of handling all these types of information.  It may interpret the 48 bits of a word in groups of four for the purpose of binary-coded-decimal operation, in groups of six for alphanumeric operation, or as individual units of information for pure binary operation.  It may also interpret the 48 bits as a mantissa and an exponent for floating-point operation.  Figure III-1 illustrates the structures of these different words.

A decimal word in the Honeywell 1800 contains either 11 decimal digits with a sign, or 12 decimal digits without sign.  The decimal arithmetic instructions interpret all operands as a sign and 11 digits.  The sign consists of four bits which may represent either the sign of the entire word or individual, 1-bit signs for as many as four different pieces of information within the word.  Although a positive sign is normally represented by four binary ones and a negative sign by four binary zeros, a non-standard configuration is perfectly acceptable as input to the arithmetic unit, which interprets any combination of bits except four binary zeros as a positive sign.  The sign supplied with the result of an arithmetic operation, however, is always one of the two standard conventions, either four binary ones or four binary zeros.  A more detailed discussion of sign conventions can be found in Section VI.

!(images/figure_III-1.png)

A Honeywell 1800 alphanumeric word comprises eight 6-bit groups.  Each group can represent any of 26 alphabetic characters, 10 decimal digits, or 20 such special characters as punctuation marks, etc., (see Table I, page 167).  Numbers may be stored in alphanumeric (6-bit) form, but the arithmetic unit cannot manipulate them as such; it handles numbers in pure binary or binary-coded decimal form.  Between the central processor and the printers, information is transferred in the alphanumeric mode; between the central processor and the card equipment, information is transmitted in either the alphanumeric or the transcription mode.

The 48 binary digits of a word may also represent a pure binary number, which may be stored as a sign and 44 bits, or as 48 unsigned bits.  With the exception of the instructions word add and word difference, which treat their operands as 48-bit unsigned numbers, the binary arithmetic instructions interpret operands as signed 44-bit numbers.  The sign convention in binary arithmetic is identical to that described for decimal words.

The Honeywell 1800 word can also be handled as a floating-point number, composed of one-bit sign, seven-bit exponent, and 40-bit mantissa.  The floating-point decimal word has an exponent that can represent a power of 10 from the -64<sup>th</sup> to the +63<sup>rd</sup>, and a mantissa that can represent a 10-digit number from .1000000000 through .9999999999 (when normalized).  In floating-point binary form (represented in hexadecimal notation), the exponent can represent a power of 16 from the -64<sup>th</sup> to the +63<sup>rd</sup>, and the mantissa a 40-bit number from .00010000...0000 through .1111...1111 (when normalized); the mantissa can represent the equivalent of approximately 12 decimal digits.  A one in the sign bit position of the floating-point word indicates that the number is positive, and a zero that it is negative.  Floating-point numbers are discussed in Section XIII.

The data words above are identified in ARGUS language by the following constant codes: DEC, fixed-point decimal number (signed or unsigned); ALF, alphanumeric word; FXBIN, fixed-point binary number; M (mixed constant), compressed alphanumeric word; FLDEC, floating-point decimal number; and FLBIN, floating-point binary number.  In addition, ARGUS recognizes an octal word identified by the constant code OCT.  This word contains 16 unsigned or 15 signed octal digits.  If 15 signed digits are specified, the most significant digit must be less than four, since a sign is represented by four bits, leaving only two bits for the high-order octal digit.

Several differences should be noted between ARGUS notation for data words and the format shown in Figure III-1.  When ARGUS notation is used for decimal words, high-order zeros in signed decimal numbers and low-order zeros in unsigned decimal numbers need not be expressed.  For example, ARGUS converts the number +125 to the signed 11-digit number +00000000125 and the unsigned number 32 to the 12-digit number 320000000000.  A binary word in ARGUS notation is not expressed as a 44- or 48-bit binary number, but as the decimal equivalent of the desired information bits.  Therefore, a binary word in ARGUS may contain up to 14 decimal digits and a sign.  For complete details on the specification of data words in ARGUS language, reference should be made to the ARGUS _Manual of Assembly Language_.

#### Special register Words

As previously noted, a special register can store 16 information bits, or one-third of a full Honeywell 1800 word.  When these bits are manipulated within the special register circuitry, the high-order bit is interpreted as a sign (1 = plus, 0 = minus).  Depending upon the type of addressing used, the remaining 15 bits of a special register word may be interpreted as a main memory address, consisting of a bank indicator and subaddress, or as a special register address, consisting of a group indicator and subaddress (see Figures IV-1 and IV-2).  When a special register word is modified arithmetically within the special register circuitry, the value of the sign bit determines whether it is incremented or decremented.  A special register word is identified in ARGUS language by the constant code SPEC.

#### Instruction Words

The 48 bits of a Honeywell 1800 instruction word are interpreted as four groups of 12 bits each.  Bits 1-12 represent the command code; bits 13-24, 25-36, and 37-48 are designated as the A address group, B address group, and C address group, respectively.  The address portions of instructions normally are used to designate the locations of operands and results, but in certain instructions they may contain special information such as the number of words to be moved, the number of bits to be shifted, a change of sequence counter, and so forth.  A detailed discussion of addressing in the Honeywell 1800 will be found in Section IV.

Machine instructions fall into five major categories: general instructions, unmasked and masked; inherent mask instructions; peripheral and print instructions; simulator instructions; and scientific instructions.  The masked general instructions and the peripheral and print instructions are uniquely designated by six-bits - bits 7 through 12 of the instruction word.  The unmasked general instructions, the inherent mask instructions, and the scientific instructions are uniquely designated by eight bits - bits 7 though 12, plus bits 2 and 3.  The simulator instructions are uniquely defined by only three bits - bits 10 through 12.  These groups of bits which uniquely specify the operation to be performed are called the operation code.  The bits of the command code which are not used for the operation code serve various other purposes which will be described as the instruction types are discussed.  A graphic summary of the format of the major command code types appears in Figure III-2.  The command codes for the individual instructions, together with their mnemonic operation codes in ARGUS language, are set forth by major instruction type in Table II, page 168.

#### General Instructions

General instructions include the arithmetic operations, logical operations, decisions, and information transfers.  As notes in Table II, certain of these instructions may only be performed without masks; others may be performed either with or without masks.  Regardless of masking, bit 1 of a general instruction command code, called the bisequence bit, always specifies the source of the next instruction (see Figure III-2).  If bit 1 is zero, the next instruction will be taken from the sequence counter; if bit 1 is a one, the next instruction will be selected from the cosequence counter.  In ARGUS language, the source of the next instruction is specified in column 23 of the ARGUS input card by an "S" or blank for sequence counter or by a "C" for cosequence counter.

#### Unmasked General Instructions

Unmasked general operation codes are specified by command code bits 2, 3, and 7 through 12.  Bits 4, 5, and 6 designate whether the A, B, and C addresses, respectively refer to a main memory or a control memory location.  If a memory designator bit is zero, then the corresponding address refers to main memory; a designator bit of one denotes a control memory address.  In ARGUS language, the memory designator bit is not explicitly stated but is implied by the type of addressing used (see Section IV).

!(images/figure_III-2.png)

#### Masked General Instructions

When general instructions are performed under the control of masks, they usually designate partial words as operands and results.  For this reason, they are frequently referred to as "field" instructions.  When a field instruction is performed, the same mask is applied to operands and result.  Only those bit positions of the operand which correspond to binary ones in the mask word are used in the operation.  The positions of the result location which do not correspond to binary ones in the mask are not altered by the operation.  The location of a mask used in a field instruction is specified by bits 2 through 6 of the command code, in conjunction with bits 2 through 5 and 11 through 16 of a special register called the mask index register (MXR).  A complete description of the way in which the five command code bits, called the partial mask address, are united with the ten bits of the MXR to designate the location of the mask will be found in Section V under the discussion of the mask index register.

In ARGUS language the location of the mask is specified by writing its symbolic tag in the command code field, following the operation code and separated from it by a comma.  Thus, the instruction
```
        DS, MASK2   WAGES   DEDUCTNS    WEEKSPAY
```
is performed under the control of the mask stored in the memory location assigned by ARGUS to the symbolic tag MASK2.  Since field instructions use the memory designator bit positions in the partial mask address, it is impossible for these instructions to address control memory.

#### Inherent Mask Instructions

The use of masks is not restricted to field instructions, but extends to the inherent mask instructions.  These instructions, which have the same command code format as the unmasked general category, include five shift instructions, a substitute, and an extract instruction.  The chief distinction between the two types of masked instructions lies in the fact that the inherent mask instructions use bits from the B address group rather than from the command code to specify the location of the mask.  For the shift instructions, the low-order six bits of the B address group are used in conjunction with bits 2 through 5 and 6 through 10 of the mask index register to locate the mask.  In the substitute and extract instructions, the entire B address group is used to specify the location of the mask, without reference to the MXR.

A further difference between inherent mask and field instructions is that the latter always operate in "protected" mode; in other words, the portions of the result location corresponding to binary zeros in the mask are preserved during the operation.  The inherent mask group, on the other hand, includes three instructions which operate in the "unprotected" mode, in which the unmasked portions of the result location are cleared to zeros.  In ARGUS language, the location of the mask for a shift instruction is specified in the same way as for field instructions: by writing its symbolic tag in the command code field following the operation code.

#### Peripheral and Print Instructions

Every instruction in the peripheral group performs some function involving a magnetic tape unit or a peripheral device.  The high-order six bits of the peripheral instruction command codes are used to specify a magnetic tape or a peripheral address.  Thus, these instructions cannot specify the source of the next instruction or address the control memory.  The peripheral address bits are divided into two groups of three bits each.  Bits 1 through 3 specify one of eight input or output channels (the operation code itself defines whether the channel is input or output) and bits 4 through 6 specify one of the devices attached to this channel.  A more detailed explanation of the assignment of peripheral address bits will be found in Section XI.

The print instructions involve the use of the console typewriter.  In this instruction, the high-order six bits of the command code are used as follows: bit 1 designates the sequence or cosequence counter as the source of the next instruction; bits 2 and 2 are irrelevant; and bits 4, 5, and 6 serve as A, B, and C address memory designators, respectively.  Thus, this instruction _can_ specify the source of the next instruction and address the control memory.

Several differences should be noted between the machine command code and ARGUS notation for these instructions.  First, the peripheral command codes in ARGUS language are reversed in terms of machine language.  In other words the mnemonic operation code is written first, followed by the device address expressed as an alphabetic code from AA to HH.  Secondly, although there is but one machine instruction for the print function, ARGUS recognizes three distinct mnemonic codes to indicate alphanumeric (PRA), hexadecimal (PRD), or octal (PRO) print format.  In machine language, the type of print format is specified by bits 5 and 6 of the B address group.

#### Simulator Instructions

Any instruction in which command code bits 10 through 12 are all ones is called a simulator instruction, since it permits the programmer to represent with a single instruction any function not built into the equipment logic, such as a machine instruction for some other data processing system.  Each such instruction provides an entry to a simulator routine which is coded by the programmer and stored beginning with the next memory location after the address specified by command code bits 2 through 12.  When the instruction is performed, it is transferred to the memory location specified by command code bits 2 through 12, the cosequence counter is set to the next higher address, and the next instruction is taken from the cosequence counter.  If bit 1 of the command code is zero, bits 2 through 12 are interpreted as a main memory subaddress.  If bit 1 is one, bits 2 through 12 are interpreted as a 3-bit index register designator and an 8-bit augmenter (see Section IV).  The address portions of a simulator instruction have no assigned function and may be used to store parameters used by the simulator routine.  The command code for an ARGUS simulator instruction is S, followed by a comma and an address designated by a symbolic tag or by an index register designator with an augmenter of seven.

#### Scientific Instructions

Eighteen of the twenty-one scientific instructions manipulate data ion floating-point form, two provide for fixed-point decimal and binary division, and one converts data between floating-point decimal form and floating-point binary form.  In an 1800 system equipped with the 1801-B option, these instructions are executed directly; in a system that does not include an 1801-B, they are interpreted as pseudo instructions that call in library routines to perform the desired operations.

The operation codes for the scientific instructions are uniquely designated by eight bits in the command code field; bits 2, 3, and 7 through 12.  Bit 1 is the bisequence bit, and bits 4, 5, and 6 are the memory designator bits referring to the A, B, and C address groups.  Thus, these instructions _can_ specify the source of the next instruction and address the control memory.

#### Special Words

Two special Honeywell 1800 words - the end-of-record word and the end-of-item word - deserve separate mention in this section.  The end-of-record word is a word whose 48 information bits are:
```
1010 1010 0000 0000 1110 1110 1110 1110 1101 1101 1101 1101
```
This word is used to designate the end of a group of words constituting a single record.  When records are being written on magnetic tape, the write operation stops only when an end-of-record word is sensed in memory.  End-of-record words are automatically generated in the central processor during execution of compute orthocount and record transfer instructions. Their function will be detailed further as these instructions are discussed.

The end-of-item word is a word whose high-order 32 bits are identical to the high-order 32 bits of the end-of-record word.  The low-order 16 bits are irrelevant for purposes of identification.  As the name implies, and end-of-item word is used to designate the end of a group of words constituting a single item within a record.  A record may contain an unspecified number of items, each of which is followed by an end-of-item word, or in the case of the last item, by an end-of-record word.  End-of-item words are automatically generated in the central processor during execution of an item transfer instruction, while certain other instructions sense for these words during execution.  Their function will be highlighted in the discussion of these instructions.








