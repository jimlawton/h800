# h800
Tools for the Honeywell H-800 and H-1800 mainframe family of computers.

The Honeywell H-800 (https://en.wikipedia.org/wiki/Honeywell_800) was a transistorized mainframe computer developed at the end of the 1950s. It was later followed by other more-powerful versions, the H-1800 and H-1800-II. 

The reason for my interest in the H-x800 family is that these were the machines that the original Apollo Guidance Computer (https://github.com/virtualagc/virtualagc) software was developed on at the MIT Instrumentation Lab (now Draper Labs). You can see the source code for the original "YUL" AGC cross-assembler, developed by Hugh Blair-Smith at MIT Instrumentation Lab, and that ran on the Honeywells here: https://github.com/virtualagc/virtualagc/tree/master/YUL.

The H-x800s were 48-bit word-size machines (with an addiitonal 8 parity bits per word), and had a 3-address instruction format, and banked memory (2048 words per bank). 

The _H-1800 Programmers' Reference Manual_ has been transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/prm/Honeywell-1800-PRM.md

The _ARGUS Manual of Assembly Language_ is being transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/argus/ARGUS_Manual_of_Assembly_Language.md
