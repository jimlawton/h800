# h800
Tools for the Honeywell H-800 and H-1800 mainframe family of computers. Initially I am working on a cross-assembler, but eventually I hope to build a simulator also.

The Honeywell H-800 (https://en.wikipedia.org/wiki/Honeywell_800) was a transistorized mainframe computer developed at the end of the 1950s. It was later followed by other more-powerful versions, the H-1800 and H-1800-II. 

The reason for my interest in the H-x800 family is that these were the machines that the original Apollo Guidance Computer (https://github.com/virtualagc/virtualagc) software was developed on at the MIT Instrumentation Lab (now Draper Labs). You can see the source code for the original "YUL" AGC cross-assembler, developed by Hugh Blair-Smith (https://www.amazon.com/Left-Brains-Right-Stuff-Computers-ebook/dp/B0192KEGUS/ref=la_B018FDP8MI_1_1?s=books&ie=UTF8&qid=1487895605&sr=1-1) at MIT/IL here: https://github.com/virtualagc/virtualagc/tree/master/YUL.

The H-x800s were 48-bit word-size machines (with an addiitonal 8 parity bits per word), and had a 3-address instruction format, and banked memory (2048 words per bank). They had 8 separate identical register banks, so that 8 programs could be run simultaneously (sort of: the ALU was multiplexed among the 8 banks). Each bank included a pair of program counters, and assembler syntax allowed instructions to specify which PC should be used for the next instruction. This is also the only architecture I've ever heard of that allowed PCs to count down as well as up.

The _H-1800 Programmers' Reference Manual_ has been transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/prm/Honeywell-1800-PRM.md

The _ARGUS Manual of Assembly Language_ has been transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/argus/ARGUS_Manual_of_Assembly_Language.md
(there are 2 pages missing in the original document scan)

## Caveats
 - No support for segments, only subsegments. YUL does not use segments. All
   code is assumed to be in the same segment.
