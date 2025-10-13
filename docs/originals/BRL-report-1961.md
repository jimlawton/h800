# HONEYWELL 800

(from https://ed-thelen.org/comp-hist/BRL61-h.html#HONEYWELL-800)

## MANUFACTURER

Minneapolis Honeywell Regulator Company 
Datamatic Division 
Newton 61, Massachusetts

 [Photo](https://ed-thelen.org/comp-hist/BRL61-0294.jpg) Photo by Minneapolis Honeywell Regulator Company 
![[Pasted image 20251013222750.png]] 
 
## APPLICATIONS 

Designed for general purpose business, businessscientific, and scientific applications, system capable of running eight programs simultaneously. 
 
## PROGRAMMING AND NUMERICAL SYSTEM

Internal number system: Binary and binary-coded decimal 
Number of binary digits/word: 48 
Number of decimal digits/word: 12 plus checking 
Number of binary digits instruction: 48 
Number of decimal digits instruction: 12 plus checking 
Number of instructions/word: 1 
Number of instructions decoded: 59 basic types 
Arithmetic system:
  Floating point (optional) 
  Fixed point (standard) 
Instruction type: Three address 
Number range…
  Decimal        nd . 10<sup xmlns="http://www.w3.org/1999/xhtml"><sup>e</sup>d</sup> -64 <= ed <= 63 
            -(1-10<sup xmlns="http://www.w3.org/1999/xhtml">-10</sup>) <= n<sub xmlns="http://www.w3.org/1999/xhtml">d</sub> <= (1-10<sup xmlns="http://www.w3.org/1999/xhtml">-10</sup>) 
  Binary.           n<sub xmlns="http://www.w3.org/1999/xhtml">b</sub> . 2<sup xmlns="http://www.w3.org/1999/xhtml"><sup>e</sup>b</sup> -64 <= e<sub xmlns="http://www.w3.org/1999/xhtml">b</sub> <= 63 
            -(1-2<sup xmlns="http://www.w3.org/1999/xhtml">-39</sup>) <= n<sub xmlns="http://www.w3.org/1999/xhtml">b</sub> <= (1-2<sup xmlns="http://www.w3.org/1999/xhtml">-39</sup>)


![[Pasted image 20251013223237.png]]
[Diagram by Minneapolis-Honeywell Regulator Company](https://ed-thelen.org/comp-hist/BRL61-0295.jpg) 

Instruction and information word format 

Word Structure - The Honeywell 800 word consists of 54 bits, of which six are used for checking. The 48 information bits may represent an 11-decimal digit number with its sign, several smaller decimal numbers, with signs for each, eight alphabetic characters, or a combination of these. A word may also be interpreted as a 44-bit binary number with its sign, or as an instruction. Using the floating-point option, a word may represent a sign bit, a seven bit exponent, and a 40-bit mantissa in binary form. 

![[Pasted image 20251013223344.png]]
[HONEYWELL 800 WORD STRUCTURE](https://ed-thelen.org/comp-hist/BRL61-0295-a.jpg) 

Instructions - In the instruction word, the information bits are divided logically into four sections which are interpreted as an operation code followed by three addresses. 

Instruction Word 
+--------------+------------+-----------+-----------+ 
|    Operation      | Address       | Address      | Address      |
|        Code          |       A              |       B             |      C            |
+--------------+------------+-----------+-----------+ 
| 12 bits               | 12 bits           | 12 bits         | 12 bits        | 
+--------------+------------+-----------+-----------+ 

Indexing - Each address in an instruction may be designated as absolute or indexed. A total of eight index registers are available to each program. 

Masking - The ability to mask words allows most internal processing instructions in the Honeywell 800 to work with fields of variable length. Each program may designate a group of 32 memory locations as masking registers. Such a designation may be changed by the programmer at say point in his program. Thus, an essentially unlimited number of masking registers is at his disposal. 

Automatic built-in subroutines
  Exponential Overflow 
  Exponential Underflow 
  Division over Capacity 
  Addition or Subtraction Overflow 
  Read or Write Error 
  Begin or End of Tape 
  Parity Failure

Automatic coding 
  Argus (Automatic Routine Generating and Updating System) 
  Fact (Fully Automatic Compiling Technique) 
  Algebraic Compiler 
  Library of Subroutines 
  Executive Routine

Registers and B-boxes
  64 Index Registers 
  8 Mask Index Registers 
  32 Input-Output Control 
  32 Sequencing and History 
  96 Special (Programmers Usage) 
  8 Automatic Subroutines 
  16 Internal Control 
  Accumulator Register 
  Low Order Product-Quotient Register 
  Mask Constant Storage Register 
  Program Control Register 
  Machine Control Register 

## ARITHMETIC UNIT 
             Incl. Stor. Access
             Microsec. 

  Add time        24 
  Mult time       162 
  Div time         450 
  Construction, arithmetic unit only 
    Vacuum tubes None 
    Transistors 2,000 
    Condenser-Diodes 10,000 diodes 
  Arithmetic mode Parallel-Serial-Parallel 
  Timing Synchronous 
  Operation Concurrent 

## STORAGE

 Access 
  Medium               No. of Words                No. of Digits               Microsec 
  Ferrite Cores      Up to 32,000                Up to 384,000          2.1 
  Magnetic Tape 
    No. of units that can be connected 64 Units 
    No. of chars per linear inch 533 Chars/inch 
    No. of decimal digits per linear in. 800 dd/inch 
    Channels or tracks on the tape 10 Tracks/tape 
    Blank tape separating each record 0.66 Inches 
    Tape speed 120 Inches/sec 
    Transfer rate 64,000 Chars/sec 
    Decimal digit transfer rate 96,000 dd/sec 
    Start time 3.5 Millisec, 
    Stop time 3.5 Millisec 
    Average time for experienced operator to change reel 30 Seconds 
    Physical properties of tape 
      Width 3/4 Inches 
      Length of reel 2,400 Feet + leaders 
      Composition 1.5 mil mylar 

## INPUT

  Media                             Speed 
  Punched Cards            240 cards/min
                    650 cards/min 
  Paper Tape                   200 chars/sec 
                    1,000 chars/sec 

## OUTPUT 

  Media                              Speed 
  Punched Cards             100 cards/min 
                     250 cards/min 
  Printer                             150 lines/min 
                     900 lines/min 
  Paper Tape                    60 chars/sec 
  
## CIRCUIT ELEMENTS OF ENTIRE SYSTEM

Type             Quantity 
Diodes         30,000 
Transistors  6,000 
Above excludes peripheral equipment 

## CHECKING FEATURES

Verification of all data transmission, arithmetic processes, address modification, memory selections, and central processing. Orthotronic correction of tape data and marginal checking for preventive maintenance. 

## POWER, SPACE, WEIGHT, AND SITE PREPARATION

Power, computer                  32 Kw        57 KVA       0.80 pf 
Capacity, air conditioner     9.11 Tons 
Weight, computer                15,720 lbs 

Requirements for the physical installation of a typical system are approximately as follows: 
  Data Processing Area 1,200 square feet 
  Service Engineering Area 400 square feet (including parts storage) 
  Ceiling Height 8 feet 
  Floor Load Capacity 75 lbs/square feet (max) 
  
  It is recommended that a raised floor be installed over the existing base floor for the protection of interconnecting cables. This floor should be a free- access type, 9 inches high with a minimum of 5 1/2 inches clearance underneath for accomodating cables. 
  
## PRODUCTION RECORD

Deliveries start in December 1960. 

## COST, PRICE AND RENTAL RATES

Figures given are for a typical system. 
Basic system, including a Central Processor, 4,096 words of memory, High-Speed Printer Type Control, High-Speed Card Reader, Six Magnetic Tape Units, High Speed Card Punch, Printer-Card, Reader-Card Punch Control. 
Purchase price                                           $975,000 
Floating-point option                                   101,800 
Additional memory blocks                          153,600 (4,096 words/block) 
Rental, basic system above, monthly         20,665 
Rental, floating point option, monthly           2,100 
Rental, additional memory blocks                 3,200 

Maintenance service contract available.

## PERSONNEL REQUIREMENTS

Personnel requirements depend on equipment configuration and application. Complete training courses for programming and operating staff included with purchase and rental charge. 

## RELIABILITY, OPERATING EXPERIENCE, AND TIME AVAILABILITY

Each unit and entire system incorporate fail-safe checking. Special construction techniques minimize cold-solder joints and intermittent contacts. All units are designed for simplicity of maintenance and speed of replacement of parts. 

## ADDITIONAL FEATURES AND REMARKS

Outstanding features include parallel processing, traffic control, system modularity, outstanding system reliability, open-ended design, automatic programming aids (FACT, ARGUS, Algebraic compiler). 
Unique system advantages include ability to run up to 8 programs simultaneously without any special programming or special instructions. 

Special procedures for magnetic tape labelling, storing, shipping, and protection from humidity, temperature, electrical, fire, or other damage are that relative humidity in area should be held at approximately 40% to insure maximum tape life, dry bulb temperature shall not exceed 74<sup xmlns="http://www.w3.org/1999/xhtml">o</sup>F, and wet bulb temperature shall not exceed 59<sup xmlns="http://www.w3.org/1999/xhtml">o</sup>F. 

## INSTALLATIONS

  Army Map Service 
  6500 Brooks Lane 
  Washington 25, D. C. 
  
  Ames Research Center 
  Moffett Field, California (Anticipated) 
  
  AVCO Corporation 
  Crosley Division 
  1329 Arlington Street 
  Cincinnati 29, Ohio (Proposed)
