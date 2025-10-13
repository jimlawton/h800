## Honeywell 800 (1958)

Original by Mark Smotherman (copied from https://people.computing.clemson.edu/~mark/h800.html)

### Summary

This early multithreaded machine implements eight virtual processors, each having 2 program counters (for coroutine structure) and an individual interrupt vector base register. On each memory cycle the hardware scans on a priority basis for activity on up to eight input controllers, then up to eight output controllers, and then the CPU. Within the CPU the hardware scans the virtual processors in a cyclic manner. Once selected, an instruction from a virtual processor executes to completion.

---

### History

The Datamatic Division of Honeywell (Minneapolis) announced the H-800 in 1958. The first installation occurred in 1960. A total of 89 were delivered.

### Highlights

- **Noteworthy**
	Hardware time-sharing (multithreading) of 8 symmetric virtual processors and up to 16 I/O controllers.- Auto-incrementing and auto-decrementing of address registers.
- **Peculiarities**
	- Base address registers for interrupt vectors (from STRETCH?).
	- Co-routine control structure implemented by two sequence counters (similar to the two-PC structure of the NBS SEAC and DYSEAC in early 1950s).
	- One-level automatic subroutine control structure implemented by one history register for each sequence counter (the history counter is loaded with a return address upon every branch).
	- Scatter-gather I/O (i.e. multiple blocks, independently located in memory) by two registers: current block address register and list address register pointing to list of initial block addresses; lack of count specification forces a special end of block symbol in the code space.

### Instruction Formats

3-address instructions

### Spaces and Addressing

48-bit word, 8 6-bit characters per word

### Working and control storage

Each virtual processor has an independent set of 32 registers:

- block of 8 index registers
- block of 16 indirect registers, 4 of which could be used for I/O:
	- 1 input block address register - auto-increment or decrement by 1 after use by I/O controller
	- 1 input "distributed item counter" (address register for list of initial block addresses)
	- 1 output block address register
	- 1 output "distributed item counter"
- block of 8 control registers
	- 2 sequence counters (SC and CSC)
	- 2 history registers (SH and CSH) - used for return address storage
	- 1 base address register (U, "unprogrammed transfer register") giving location of interrupt vector
	- 1 mask index register (MXR)
	- 2 arithmetic control counters - used for multiply step counts and block length counts

### Memory name-space and hierarchy

128K words maximum (in practice 32K words).

### Address calculation and addressing modes

Two modes: index and indirect.

### Address mapping

None. A follow-on design, the H-8200, had relocation registers.

### Data Formats

**Character** - 6-bit characters (zone bit encoding)

### Operations

### Sequencing

**Normal sequencing** is by one of two sequence counters; each instruction has a bit indicating from which SC to take the next instruction address.

**Delegation** (subroutine call) is implemented using the history registers, which are loaded with the return address link whenever a branch is taken.

### Supervision

**Control switching.**
Normally, for each memory cycle, the hardware performs an activity scan on the 8 output controllers, then the 8 input controllers, then the central processor. The first one that indicates a need gets the memory cycle, and the scan begins again from the start for the next cycle. Within the central processor, normally memory cycle distribution is cyclical by active virtual processor. However, when an instruction is initiated, it must be completed - usually 4 memory cycles (maybe more, counting cycles stolen by the I/O controllers), and there are some instructions that leave information in shared registers (such as a low-order product in a multiply) that force the next instruction to come from the same virtual processor.

The basic control instruction is MPC (multiprogram control), which allows virtual processors to be turned on and off.

### Integrity

No memory protection and one mode of operation; the design assumes cooperative processes since one virtual processor can disable the other processors to monopolize the memory cycles. A follow-on design, the H-8200, added a monitor mode and relocation registers.

### Input/Output

A READ instruction executed by a virtual processor started I/O. A second READ to an invalid address (all ones) caused the virtual processor to stall until the original I/O was completed.

### Comments

The H-800 design was part of a family of 48-bit word, three-address instruction format computers that descended from the [Datamatic 1000](http://www.cs.clemson.edu/~mark/d1000.html), which was a joint Honeywell and Raytheon project started in 1955. Only about eight D1000s were built; each weighed 25 tons, required 6,000 square feet, and cost $1.5M. The D1000 and [H-400](http://ed-thelen.org/comp-hist/BRL64-h.html) family members were decimal machines, while the H-800 members included binary.

The [1800 and 1800-II](http://ed-thelen.org/comp-hist/BRL64-h.html#HONEYWELL-1800) were follow-on designs to the H-800. Also, the H-8200 was a later machine (announced 1965, possibly in response to IBM S/360) with:

- memory protection - a key on each 512-word block and read/ write/execute access rights on each block; thus shared subroutines stored under key 0 for free access, but with execute only rights
- dynamic memory relocation - base registers
- two modes of operation - privileged instructions to change memory keys and base registers

It combined a H-4200 (character-oriented machine), an H-800 (word-oriented machine), and a 9th H-800 virtual processor with master mode capabilities for use by a control program.

The character-oriented processor acted as a communications front- end and also a tightly-coupled spooling processor; it operated in parallel and interrupted the other processor, forcing it into master mode.

A monitor call instruction was added to the H-800 architecture to allow invocation of the master mode virtual processor by the other virtual processors. The master mode virtual processor was used for initial job scheduling, memory allocation, base register modification, and interprocessor communication. It was not used for dispatching since that was performed in the hardware. The master mode was also differentiated into "hunt" and "no-hunt" modes, the latter meaning that hardware time-sharing was disabled and the master mode processor monopolized the memory cycles.

---

From Julian Thomas (jt at [jt-mj.net](http://jt-mj.net/)):

> The D1000 never had two sequence counters. What it did have was the capability on a number of instructions of doing a *subsequence* call - this did not change the sequence counter,
> 
> Consider the following instructions:
> 
> ```
> 1100  ADD  A  B  C
> 1101  TXS  x  y  1200
> 1102  SUB  A  B  C
> ...
> 1200  ADD  counter =1 counter
> ```
> Actual sequence: 1100 1101 1200 1102
> 
> Note that if 1200 had done a sequence call, we never would have gotten to 1102. If 1200 had another subseq call, that instruction (repeat until bored) would also have been executed before 1102.
> 
> The 800 replaced the concept of the subsequence call with the presence of a real second counter; as you note, a bit in each instruction specifies which counter is used for the next instruction.
> 
> TS a b c (cs counter next instruction) branches to c using the cs counter. If instruction at c specifies sc for next instruction, this has the same effect as the D1000 TXS.
> 
> ...
> 
> The \[H-800\] console used a typewriter (IBM mechanism, electric typewriter before selectric); there were very few indicators (I think for each virtual CPU there was an active indicator) - one was a 5 position control error indicator (it stopped on error) - usually caused by program malfunction (illegal op or addressing). I remember that all 5 being on was called a full house and was fairly common.
> 
> A console print (write to operator) would be preceeded by a digit indicating which control group (virt cpu #) originated it. Normally it was a single word followed by a CR, but there was a way to hold the typewriter and print the next word right after the previous 8 characters (and another way to put a carriage return into this). One of my colleagues shared a mischevious bent with me - we programmed into one of our runs something to make it appear as if it were printing from control group 8 or 9 - calling on the service engineer by name
> 
> 8 FIXME  
> 9 BAKER!
> 
> Another quirk was that they used some typebars for special symbols, and remapped the letter J to a shifted character. I tended to name many of my programs JTxxxx... and noticed the stutter. Needless to say, my colleague and I immediately renamed a program JJJJANET (after another one of the programmers - the one who wrote the "squisher" for FACT that moved stuff in memory).
> 
> IO - tapes: nice 1" wide, with vacuum capstan and columns with a plug panel for address reassignment. Most shops this panel was a rats nest, with drives being constantly reassigned by plugging. A monitor I wrote did it all by software; I always set the panel up 1:1.
> 
> The tapes had a long (2k word??) rewriteable block at the front, with a special mark (optically sensed) to designate the start of the rest of the information; this allowed a directory or whatever to be written at the front of the tape without messing up the following data.
> 
> Unit record was card - IBM gear (a collator for input; probably a 519 punch for output). There was a fast (for the period - 600lpm) line printer (a rotating drum with the characters on it; print hammers behind the paper). I don't remember who built the printer.
> 
> ...
> 
> I should also have mentioned "Orthotronic Control" - Dick Bloch's invention for the D1000 for tape error correction. It used an extra track (the 1000 tapes were fixed block length - 62 words, 3" wide, with 31 channels (i.e. RW heads) across the tape. There must have been a 32nd (or 33rd; one was probably used for block marks/synch or other housekeeping) channel available and it was used for the correction, which IIRC was fairly transparent to the software.
> 
> H800 tapes were mechanically descendants of the D1000 tapes (which kicked the stuffing out of IBM tapes for tape sorts in its day) but 1" wide, with fewer RW heads; so the ortho control was pushed into the software. When a block of data was ready to be written, an EOR word was put at the end of the block, and the CO instruction (Compute Ortho) against the block (it handled the gather write situation where the block wasn't simple contiguous), replacing the EOR word and the 2 following words with 2 ortho words (think checksum) and a new EOR word.
> 
> I don't remember exactly how the software tape error correction process worked.
> 
> I'm told that there was one instance of an ortho word actually coming out to be a real EOR word which, of course, caused the tape record to be a word or 2 short. Took several days for the wizards (I was gone by then) to figure that one out.
> 
> All of the unit record stuff used on the D1000 was replaced with different stuff for the H800. Also, the 1000 had offline unit record IO; the H800 was all online, and they used spooling or direct IO.
> 
> They made divide an extra cost option on the H800, but I think almost everyone had it.

---

### References

- H.W. Schrimpf, "Information Handling Apparatus," US Patent 3,029,414, filed August 11, 1958, granted April 10, 1962.
- N. Lourie, H. Schrimpf, R. Reach, and W. Kahn, "Arithmetic and control techniques in a multiprogram computer," in Proc. EJCC, 1959, pp. 75-81.
- S.D. Harper, "Automatic parallel processing," in Proc. Conf. Computing and Data Processing Society of Canada, 1960, pp. 321-331.
- [H800 Programmer's Reference Manual, 1960](http://www.textfiles.com/bitsavers/pdf/honeywell/h800/H800_programmersRefMan.pdf) (11 MB pdf file, from Al Kossow's on-line collection)
- [Martin H. Weik, "A Third Survey of Domestic Electronic Digital Computing Systems," Ballistic Research Laboratories, Report No. 1115, March 1961](http://ed-thelen.org/comp-hist/BRL61-h.html#HONEYWELL-800) (ed-thelen.org)
- B.A. Maynard (ed.), "Honeywell 800 System," in Manual of Computer Systems. London: Gee and Company, 1964.
- J. Bouvard, "Operating system for the 800/1800," Datamation 10, 5 (May 1964) 29-34.
- T.C. Cull, "The Honeywell 8200," Datamation 11, 7 (July 1965) 90-91.
- N. Nisenoff, "Scratchpad memories at Honeywell: Past, present, and future," Proc. AFIPS FJCC 1965, pp. 679-688. \[includes overview of H-800 and H-8200\]
- T.F. Hatch and J.B. Geyer, "Hardware/software interaction on the Honeywell Model 8200," in Proc. AFIPS FJCC, 1968, pp. 891-901.
- references to H-8200 in: C.C. Foster, Computer Architecture. NY: Van Nostrand Reinhold, 1970.
- Julian Thomas, [Datamatic 1000](http://www.cs.clemson.edu/~mark/d1000.html).

---

### Acknowledgement

Many thanks to Julian Thomas for his help in understanding the H800.

---

[\[Multithreading page\]](http://www.cs.clemson.edu/~mark/multithreading.html) [\[History page\]](http://www.cs.clemson.edu/~mark/hist.html) [\[Mark's homepage\]](http://www.cs.clemson.edu/~mark/homepage.html)
