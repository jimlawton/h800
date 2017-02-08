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

                                                                           Page
Section I       Introduction ..............................................   1
                    Programming Aids ......................................   1
                    Fixed-Point Numbers ...................................   2
                    Decimal System ........................................   2
                    Binary System .........................................   2
                    Binary Codes ..........................................   3
                    Octal and Hexadecimal Systems .........................   3
                    Floating-Point Numbers ................................   3

Section II      The Honeywell 1800 System .................................   5
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

Section III     The Honeywell 1800 Word ...................................  27
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

Section IV      Addressing ................................................  35
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

Section V       Special Registers .........................................  51
                    Sequencing Counters ...................................  54
                    History Registers .....................................  56
                    Index Registers .......................................  56
                    Mask Index Register ...................................  57
                    General Purpose Registers .............................  58
                    Read-Write Counters ...................................  58
                    Arithmetic Control Counters ...........................  60
                    Unprogrammed Transfer Register ........................  61

Section VI      Arithmetic Instructions ...................................  65
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

Section VII     Logical Instructions ......................................  75
                    Extract, EX ...........................................  75
                    Substitute, SS ........................................  76
                    Half Add, HA ..........................................  77
                    Superimpose, SM .......................................  77

Section VIII    Transfer Instructions .....................................  79
                    Transfer A to C, TX ...................................  80
                    Transfer and Sequence Change, TS ......................  80
                    N-Word Transfer, TN ...................................  81
                    Multiple Transfer, MT .................................  82
                    Record Transfer, RT ...................................  83
                    Item Transfer, IT .....................................  83

Section IX      Decision Instructions .....................................  85
                    Inequality Comparison, Alphabetic, NA .................  86
                    Less Than or Equal Comparison, Alphabetic, LA .........  87
                    Inequality Comparison, Numeric, NN ....................  87
                    Less Than or Equal Comparison, Numeric, LN ............  87

Section X       Shift Instructions ........................................  89
                    Shift Preserving Sign and Substitute, SPS .............  91
                    Shift Preserving Sign and Extract, SPE ................  91
                    Shift Word and Substitute, SWS ........................  91
                    Shift Word and Extract, SWE ...........................  92
                    Shift Word and Select, SSL ............................  92

Section XI      Peripheral Instructions ...................................  95
                    Read Forward, RF ......................................  97
                    Read Backward, RB ..................................... 100
                    Write Forward, WF ..................................... 102
                    Rewind, RW ............................................ 105

Section XII     Miscellaneous Instructions ................................ 107
                    Print, PRA, PRD, PRO .................................. 107
                    Control Program, MPC .................................. 109
                    Proceed, PR ........................................... 114
                    Simulator, S .......................................... 114
                    Compute Orthocount, CC ................................ 116
                    Check Parity, CP ...................................... 117

Section XIII    Scientific Instructions ................................... 121
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

Section XIV     Summary of Instructions ................................... 137
                    General Instructions, Unmasked or Masked .............. 137
                    General Instructions, Unmasked ........................ 138
                    Inherent Mask Instructions ............................ 139
                    Peripheral and Print Instructions ..................... 140
                    Simulator Instructions ................................ 141
                    Scientific Instructions ............................... 141

Appendix A.     Fixed-Point Addition in the Honeywell 1800 ................ 145

Appendix B.     Orthotronic Control ....................................... 149

Appendix C.     Timing Summary ............................................ 155

Appendix D.     Control Errors ............................................ 165

Appendix E.     Tables .................................................... 167

Appendix F.     Memory Extensions beyond 32,768 Words ..................... 169

Appendix G.     Memory Barricade .......................................... 173


## LIST OF ILLUSTRATIONS

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

    1. The Central Processor (1801)

    The basic central processor consists of a control unit, a control or special-register memory, an arithmetic unit, and four banks of main (or high-speed) memory, each able to store 2048 Honeywell 1800 words.  (A Honeywell 1800 word is composed of 48 information bits and six checking bits.)  To this basic unit, additional memory banks can be added in modules of 8192 words (model 1802) up to 32,768 words; further expansion is available in modules of 16,384 words (model 1802-1) up to a maximum of 65,536 words.  An optional floating-point unit (1801-B, discussed below) is also available.

    The control unit with its control memory is the nerve center of the central processor.  As the site of traffic control and multiprogram control (explained below), it monitors the time sharing of the entire system to achieve maximum efficiency of operation.  In addition to its multiplexing function, it is also the unit that selects, interprets, and directs the execution of instructions, and governs address selection in both control memory and main memory.

    The memory cycle time is two microseconds.  This is the time required to read one Honeywell 1800 word from memory (access) and to replace it in its original form (restoration).

    The control memory is a magnetic-core array providing storage for 356 eighteen-bit words.  The read-restore cycle of the control memory is out of phase with that of the main memory in such a way that if reference must be made to the control memory between references to main memory, it is usually possible to make such reference without loss of main-memory cycle.  As discussed more fully in Section V, the control memory contains eight identical groups of special registers such as sequencing counters, index registers, registers used for indirect addressing, etc., the contents of which are used to select a full Honeywell 1800 word from the main memory.  The offset cycle of control memory makes it possible to anticipate an address selection involving the contents of a special register and to prepare the address of a second operand while another unit is using the first operand.  Because of this anticipatory technique, it is unnecessary in many cases to add memory cycles to an instruction for indexed or indirect addressing.  Even when the contents of a special register are modified before they are restored, no extra memory cycle need be added, since the special register circuitry includes a separate adder, with complete and independent checking, used only for special register modification.  This applies to both automatic modification, as when a sequencing counter is incremented after use, and program-controlled modification, as when an increment is specified in an address.  However, while the two memory units are sufficiently out of phase to allow reading from the control memory prior to the start of a main memory cycle, a read-restore operation in which the result of an instruction is returned to a special register cannot overlap a main memory cycle; in this case, an extra cycle must be added to the instruction time.

    The arithmetic unit is the portion of the central processor in which digits are combined to form new arrays in accordance with the logical rules of the command codes.  The Honeywell 1800 central processor has provision for both binary and decimal arithmetic, complete logical abilities, and competent internal checking.  For the interested reader, a complete description of the fixed-point addition logic can be found in Appendix A.

