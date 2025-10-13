# Honeywell 1800 Specification Extraction (Initial Draft)
# Path: h800/docs/h1800-spec.md
# Status: Draft – incomplete; placeholders marked TODO.
# Purpose: Capture concrete, minimally ambiguous architectural elements required
#          for implementing the instruction-set simulator prior to full manual transcription.

---

## 1. Scope & Sources

This document consolidates the essential low‑level architectural elements extracted from the Honeywell 1800 Programmers’ Reference Manual outline and existing opcode metadata in the project.  
Where precise bit layouts or numeric limits are not yet confirmed by the primary source, items are marked TODO with assumptions kept explicit.  
This draft is intended to unblock simulator scaffolding (register files, instruction decode, addressing resolution) while deferring ambiguous areas (floating‑point formats, advanced control features, multiprogram sequencing nuances).

---

## 2. Fundamental Word Sizes

| Entity | Nominal Width | Notes |
|--------|---------------|-------|
| Instruction word | 12 bits | All executable opcodes; fetched sequentially. |
| Data word | 48 bits | Used for arithmetic, memory storage, peripheral buffers (per existing codebase). |
| Mask field (masked instructions) | 5 bits | Occupies bits 2–6 when bit7 = 1 and opcode type = maskable. |
| Peripheral address (paddr) | 6 bits | Occupies bits 2–6 for peripheral instructions (bit7 = 1). |
| Opcode field | 5 bits | Bits 8–12 (value range 0–31 octal 0o00–0o37). |

TODO: Confirm whether the 48‑bit data word ever packs multiple 12‑bit instructions (current implementation assumes “1 instruction per fetch” – treat instruction memory as 12‑bit cells logically stored inside 48‑bit word slots or a separate store).

---

## 3. Instruction Word Bit Layout (Canonical Decode Basis)

Bit numbering: 1 (MSB) … 12 (LSB) in existing project conventions.

| Bits | Role (General Case) | Comments |
|------|----------------------|----------|
| 1    | Sequence / Cosequence bit (s) | Distinguishes sequence variant, affects control flow (e.g., TS). |
| 2–3  | Variant bits (b23) for unmasked general & inherent mask instructions | Encode subgroup/class discriminator (00,01,10,11). |
| 2–6  | Mask or Peripheral Address (paddr) or “maskable operand space” | Interpretation depends on bit7 and opcode type. |
| 4–6  | Operand flags (a,b,c) | Present only when bit7 = 0 (unmasked) OR for print/scientific/inherent instructions needing flags. |
| 7    | Masked / Peripheral / Print indicator (b7) | 1 = masked/peripheral/print forms; 0 = unmasked / inherent; simulator = None (special case). |
| 8–12 | Opcode field (op) | Base numeric opcode; collision space PRA/PRD/PRO share same op code (0o06 in existing table). |

### 3.1 Masked General Instruction Format
```
| s | mmmmm | 1 | opcode(5) |
Bit1 Bit2-6 Bit7 Bits8-12
```
- Bits 2–6: 5-bit mask value (0–31).
- Bit7 = 1.
- Operand flags (a,b,c) suppressed (not encoded).
- Applicable to: BA, DA, WA, BS, DS, WD, NA, NN, LA, LN, TX, TS, HA, SM, CP (per existing metadata).

### 3.2 Unmasked General Instruction Format
```
| s | b23 | a b c | 0 | opcode(5) |
Bit1 Bits2-3 Bits4-6 Bit7 Bits8-12
```
- Bits2–3: variant group (00–11).
- Bits4–6: operand presence flags a,b,c (0/1).
- Bit7 = 0.

### 3.3 Inherent Mask Instructions (Shift & Extract/Select Family)
Appear structurally similar to unmasked general; mask addressing inherent to operation semantics (no explicit mask field).  
- Bit7 = 0.
- Bits2–3 may select subcategory (e.g., SWS, SPS, SWE, SPE, SSL, SS, EX).

### 3.4 Peripheral Instruction Format
```
| paddr(6) | 1 | opcode(5) |
Bits1-6 Bit7 Bits8-12
```
- Paddr: 6-bit peripheral address (0–63).
- Bit7 = 1.
- No sequence or operand flags (sequence bit repurposed as part of paddr).
- Instructions: RF, RB, WF, RW.

### 3.5 Print Instruction Format (Collision Space)
```
| s | xx | a b c | 1 | opcode(5) |
Bit1 Bits2-3 Bits4-6 Bit7 Bits8-12
```
- Bits2–3 treated as don’t care (xx) for decode grouping.
- PRA, PRD, PRO share identical numeric opcode & layout (distinguished only by mnemonic at assembly time).

### 3.6 Simulator Instruction Format
- Opcode field: 0o07 (decimal 7).
- Bit7: None / ignored.
- Two recognized words: with sequence bit 0 (0o0007) and sequence bit 1 (0o4007).
- Other bits treated as don’t care or fixed zeros.  
TODO: Confirm additional simulator sub-modes (direct vs indexed) if manual distinguishes.

### 3.7 Scientific Instruction Formats
Follow unmasked pattern (variant bits + operand flags) or extended precision patterns (FBAE/FBSE/etc.) sharing underlying layout:
```
| s | variant(2) | a b c | 0 | opcode(5) |
```
TODO: Confirm exact variant mapping and whether any scientific op uses bit7 = 1 or special mask semantics (current table suggests unmasked type).

---

## 4. Opcode Classification (From Existing Metadata)

| Type | Bit7 | Distinguishing Field(s) | Examples |
|------|------|-------------------------|----------|
| Maskable (masked form) | 1 | Bits2–6 mask | BA, DA, … |
| Maskable (unmasked form) | 0 | Bits2–3 variant; a,b,c | Same mnemonics as above |
| Unmasked (general) | 0 | Bits2–3 variant; a,b,c | BM, DM, MT, TN, CC, IT, EBA, EBS, RT, MPC, PR |
| Inherent mask | 0 | Bits2–3 variant; a,b,c | SS, EX, SWS, SWE, SPS, SPE, SSL |
| Peripheral | 1 | Bits1–6 paddr | RF, RB, WF, RW |
| Print | 1 | PRA/PRD/PRO share op; a,b,c & sequence significant | PRA, PRD, PRO |
| Simulator | (None) | Sequence distinguishes forms | S |
| Scientific | 0 | Bits2–3 variant; a,b,c | FBA,FBS,FDA,FDS,... (extended & unnormalized forms) |

---

## 5. Addressing Modes (Extraction Outline)

| Mode | Description | Required Fields | Steps |
|------|-------------|-----------------|-------|
| Direct Memory | Use address as given | 12-bit logical address | Fetch data word directly |
| Direct Special Register | Address maps into special register space | Special range mapping | Translate address to register index |
| Indexed | Base + index register value | Base address + index register | Add index, mask to address range |
| Indirect | Address points to pointer word | Base address | Fetch pointer word, re-resolve |
| Indexed Indirect | Indexed first, then indirect dereference | Base + index | Apply index → fetch pointer → final |
| Extended Memory | Address beyond base segment mapped via bank bits | Raw address | Compute (bank, offset) using extension scheme |
| Stopper / Inactive | Reserved or forbidden addresses | Raw address | Validation pre access; trap on violation |

### 5.1 Address Bit Partition (TODO)
Manual sections (Addressing & Memory Extensions) need detailed extraction:
- Base logical address width (likely > 12 with extension scheme).
- High-order extension bits location (maybe separate control memory registers).
- Mapping algorithm for addresses > 32,768 (Appendix F).

### 5.2 Effective Address Resolution Pipeline (Proposed)
```
raw -> (apply index if requested) -> (if indirect: dereference) -> (extension map if high range) -> validate (inactive/barricade/stopper) -> physical address
```

---

## 6. Special Registers (Preliminary List – TODO Confirm Counts/Widths)

| Register | Purpose | Width | Notes |
|----------|---------|-------|-------|
| Accumulator (A) | Primary arithmetic result | 48 bits | Used by add/sub/accumulate |
| Low-Order Product (P_low) | Multiply/Divide low part | 48 bits | Pair with high part if needed |
| High-Order Product (P_high) | Multiply/Divide high part | 48 bits | TODO confirm presence |
| Index Registers (Xn) | Indexed addressing base | 48 bits | Count unknown (assume ≥2; manual to confirm) |
| Mask Index Register (MIR) | Source for mask application | 48 bits | Supplies mask bits for masked instructions |
| General Purpose Registers (GPRs) | Temporary storage | 48 bits | Count TBD |
| Sequencing Counters | Program flow (multiprogram) | (12 or >12) bits | At least 1 primary; manual references plural (Section V) |
| History Registers | Diagnostic/trace info | TBD | TODO confirm relevance for simulation |
| Read-Write Counters | Track I/O or program metrics | TBD | Possibly optional for initial implementation |
| Arithmetic Control Counters | Overflow/underflow management | TBD | Scientific operations dependency |
| Unprogrammed Transfer Register | Facilitates specific transfer instructions | TBD | Validate usage in TX/IT/MT |
| Barricade Register | Memory protection boundary | 48 bits? | Appendix G; restricts memory access |
| Parity / Orthocount Status | Error detection | Boolean / small int | Map to control flags (simulation) |

> TODO: Extract exact bit widths & enumerations for each from full manual sections (Sequencing Counters, History Registers, Index Registers, etc.).

---

## 7. Flags & Condition Indicators

| Flag | Source Instruction(s) | Effect |
|------|------------------------|--------|
| Parity Error | CP | Set parity_error; may halt or continue (configurable) |
| Orthocount Error | CC | Set orthocount_error; triggers diagnostic path |
| Overflow | Floating & fixed arithmetic | Set overflow; optionally trap |
| Underflow | Floating arithmetic | Set underflow; optional trap |
| Halted | PR / explicit simulator stop / trap | Stops execution loop |
| Simulator Mode | S | Alters interpretation of subsequent words (if specified) |
| Barricade Violation | Memory access check | Trap & halt |
| Stopper Reached | Address equals defined stopper | Halt gracefully |

TODO: Determine whether comparisons (NA, LA, NN, LN) set condition flags or control sequencing directly (e.g., branch/skip semantics).

---

## 8. Mask Handling

- Masked instructions: bits2–6 supply a 5-bit mask, typically applied to memory operations (shift/select; confirm operational semantics).
- Unmasked variant: a,b,c flags choose memory designators (set presence bits for operand usage).
- Mask Index Register (MIR) involvement: TODO – confirm if mask field indexes into MIR or simply applied directly.

---

## 9. Floating-Point Format (Scientific Option) – Placeholder

Likely components (common mid‑century format patterns):
| Component | Tentative |
|-----------|-----------|
| Sign | 1 bit |
| Exponent | N bits (TODO: extract) |
| Mantissa | Remaining bits (normalized/unnormalized variants) |

Operations:
- Normalized add/sub (FBA/FBS/FDA/FDS).
- Unnormalized variants (FBAU, FBSU, FDAU, FDSU).
- Extended precision (FBAE, FBSE).
- Multiply/Divide (FBM, FDM, FBD, FDD).
- Conversion (FCON).
- Normalize (FFN).
- Comparison (FLN, FNN).
- Multiple Unload (ULD).
- Fixed divide (BD, DD).

TODO: Confirm:
- Exponent bias.
- Mantissa alignment rules pre/post operation.
- Overflow/underflow thresholds.

---

## 10. Memory Barricade & Protection

- Barricade Register defines upper (or range) boundary.
- Any instruction referencing memory beyond barricade triggers control error (Appendix G).
- Program Interference Protection & compatibility rules: TODO – specify algorithms for enforcement.
- Implementation plan: Validate address at effective resolution stage; raise trap on violation.

---

## 11. Stopper & Inactive Addresses

- Stopper Address: Execution halts gracefully upon fetch at stopper (TODO: numeric default).
- Inactive Addresses: Access to these triggers control error or ignore (manual section implies special handling).
- Simulator configuration will allow user to set stopper address; default=highest valid or explicit config file.

---

## 12. Instruction Timing (Appendix C – Deferred)

- Each instruction has documented timing (cycle counts).
- For initial functional simulator: accumulate approximate cycles using a lookup table.
- TODO: Extract exact timing entries; differentiate masked vs unmasked vs peripheral latency.

---

## 13. Decode Algorithm Summary (Current Implementation Basis)

1. Extract bit7, bits2–3, bits2–6, bits4–6, bits8–12.
2. Match opcode field -> candidate mnemonics.
3. Branch on type:
   - maskable: decide masked vs unmasked by bit7 and field usage.
   - peripheral: bit7=1, treat bits1–6 as paddr.
   - print: bit7=1, operand flags valid, shared collision space.
   - simulator: opcode = 0o07 regardless of bit7 (ignore mask).
   - scientific: treat as unmasked with variant bits.

4. Produce candidate list + extracted fields dictionary.

Note: PRA/PRD/PRO collision inclusion always returns all three in decode candidate set.

---

## 14. Open Questions / TODO Extraction Targets

| ID | Question | Current Assumption | Action |
|----|----------|--------------------|--------|
| Q1 | # of index registers | ≥2 | Extract from full manual Section V |
| Q2 | Floating-point layout | Unspecified | Parse Section XIII details |
| Q3 | Barricade register width & semantics | Same as data word | Confirm Appendix G |
| Q4 | Orthocount algorithm | Flag only | Extract Appendix B |
| Q5 | Parity domain | Instruction + data? | Confirm parity scope (CP) |
| Q6 | Sequence counter multi-program support | Single active PC initially | Extract Multiprogram Control section |
| Q7 | Stopper address default | User-configurable | Find location in manual (Section IV) |
| Q8 | Interaction of mask index register vs explicit mask field | Direct field use | Confirm mask index register role |
| Q9 | Are instructions ever packed multiple per data word? | No | Validate memory model in Section III |
| Q10 | Simulator instruction semantic depth | Mode toggle only | Confirm Section XII (Simulator) |
| Q11 | History registers usage | Omitted initially | Extract Section V (History Registers) |
| Q12 | Overflow/underflow recovery procedure | Halt or set flag | Extract Section XIII (Overflow/Underflow) |

---

## 15. Implementation Readiness Matrix

| Element | Confidence | Ready for Coding | Notes |
|---------|------------|------------------|-------|
| Instruction 12-bit layout | High | Yes | Bit positions stable |
| Mask vs unmasked decode | High | Yes | Existing tables adequate |
| Peripheral address mapping | Medium | Yes (stub devices) | paddr semantics fine; device set TBD |
| Print collision logic | High | Yes | Already implemented upstream |
| Basic arithmetic ops | Medium | Yes | Semantics rely on 48-bit words |
| Shift/extract/select ops | Medium | Yes | Need exact bit behavior definitions (spec soon) |
| Addressing resolution pipeline | Low-Med | Partial | Requires index register spec & indirect depth rules |
| Memory extensions | Low | No | Extract Appendix F details first |
| Floating-point ops | Low | No | Need full format specification |
| Barricade protection | Medium | Partial | Basic boundary check workable; details pending |
| Traps & flags | Medium | Yes (scaffold) | Exact conditions may expand later |

---

## 16. Next Steps

1. Produce a “spec delta” extraction pass over:
   - Section V (All special registers).
   - Section IV (Addressing forms & inactive/stopper address definitions).
   - Appendix F (Memory extensions mapping).
   - Section XIII (Scientific instructions & floating-point format).
   - Appendix G (Barricade operation).
2. Convert open questions Q1–Q12 into discrete GitHub issues (or project tracker tickets).
3. Lock this draft as v0.1; update as details finalize.

---

## 17. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 (draft) | YYYY-MM-DD | (auto-generated) | Initial extraction skeleton |
| 0.2 | TODO | TODO | Populate confirmed register counts |
| 0.3 | TODO | TODO | Add floating-point format & timing table |
| 1.0 | TODO | TODO | Complete spec for simulator implementation phase |

---

## 18. Disclaimer

All TODO and assumption markers must be validated against the full Honeywell 1800 Programmers’ Reference Manual before declaring functional equivalence. This document intentionally favors clarity for implementation over historical verbatim reproduction; exact wording & diagrams should be added in later revisions.

---

*End of initial specification draft.*