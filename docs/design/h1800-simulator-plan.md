# Honeywell 1800 Instruction-Set Simulator Design Plan

## 1. Objectives

Build a functionally accurate (optionally timing‑aware) simulator for the Honeywell 1800 computer architecture, supporting:
- Full 12‑bit instruction set execution on 48‑bit data words.
- All instruction classes: arithmetic, logical, transfer, decision, shift, peripheral, print, simulator, scientific.
- Complete addressing modes (direct, indexed, indirect, indexed‑indirect, special register, memory extension).
- Memory initialization from multiple sources (binary/octal dumps, assembler listings, structured JSON/YAML).
- Pluggable, file‑backed peripheral device emulation.
- Execution control (run, halt, single-step, breakpoints, traps).
- State introspection (registers, memory, disassembly, trace).
- Save/restore snapshots for reproducible debugging.

## 2. Architectural Overview

| Layer | Responsibility |
|-------|----------------|
| CPU Core (`cpu`) | Fetch/decode/execute, sequencing counters, traps, stepping |
| Decoder (`decoder`) | Convert 12‑bit words to structured instruction objects (reusing opcode metadata) |
| Executor (`executor`) | Implement semantics for each opcode category via a dispatch table |
| Memory (`memory`) | 48‑bit word storage, extensions (Appendix F), barricade enforcement |
| Registers (`registers`) | Special registers (accumulator, product, index, mask index, sequence counters, control flags) |
| Devices (`devices`) | Peripheral abstractions (tape, card reader/punch, printer, paper tape, random access storage, clocks) |
| Loader (`loader`) | Ingest external images/listings into memory |
| Traps/Errors (`traps`) | Centralized exceptions (parity, orthocount, overflow, barricade, control errors) |
| Simulator Orchestrator (`sim`) | High-level API (run, step, attach devices, snapshots) |
| CLI (`cli`) | Interactive control shell & batch operation |
| State (`state`) | Serialization/deserialization of full simulator state |

## 3. Core Data Structures

### 3.1 Instruction Representation

```text
Instruction {
  raw_word: int (0..0o7777)
  mnemonic: str
  type: Enum(masked, unmasked, inherent_mask, peripheral, print, simulator, scientific)
  fields: { sequence?, mask?, a?, b?, c?, paddr?, index?, … }
  effective_address: Optional[int]
  cycle_cost: Optional[int]
}
```

### 3.2 CPU State

```text
CPUState {
  pc: int                   # Program counter (or sequence counter)
  sequence_counters: [int]  # Multiprogram counters (size configurable)
  accumulator: int          # 48-bit
  product_low: int          # 48-bit
  product_high?: int        # Optionally if architecture splits 96-bit product
  index_registers: [int]    # Confirm count from manual
  mask_index_register: int
  general_purpose_registers: [int]
  control_flags: {
    parity_error: bool
    orthocount_error: bool
    overflow: bool
    underflow: bool
    halted: bool
    simulator_mode: bool
  }
  barricade_register?: int
  error_status?: int
  trace_enabled: bool
}
```

### 3.3 Memory Model

- Primary memory: `words: list[int]` (masked to 48 bits).
- Extension map: `extended_banks: dict[bank_id, list[int]]`.
- Accessor: `read_word(address) -> int` resolves extension + barricade.
- Write path validates stopper & inactive ranges (Section IV).

### 3.4 Device Interface

```text
class Device:
    name: str
    def read(self, request) -> bytes | list[int]
    def write(self, request, data) -> None
    def rewind(self) -> None
    def status(self) -> dict
```

Concrete devices implement `request` semantics (block numbers, record IDs, line indices).

## 4. Execution Pipeline

1. **Fetch**: Read 12‑bit instruction word from memory at `pc`.
2. **Decode**: Lookup opcode meta, construct `Instruction`.
3. **Address Resolution**:
   - Apply indexing, indirect referencing, memory extension mapping.
   - Validate against inactive/barricade/stopper addresses.
4. **Execute**: Use dispatch map `{ mnemonic: handler }`.
5. **Update PC / Sequence Counters**:
   - Default increment.
   - Transfer instructions modify PC (TX, TS, MT, TN, IT, RT).
   - Simulator instruction (S) toggles mode affecting stepping.
6. **Check & Trap**:
   - Parity (CP), Orthocount (CC), overflow/underflow (scientific), barricade violation.
   - On fatal trap: set `halted` & record reason.
7. **Post‑Execution Hooks**:
   - Trace logging (if enabled).
   - Watchpoints (memory/register changes).
8. **Loop** until halted or external stop.

## 5. Addressing Modes (Planned Implementation)

| Mode | Steps |
|------|-------|
| Direct | Use address field as physical/logical address |
| Special Register | Map address space slice to register indices |
| Indexed | Add selected index register value (mod address range) |
| Indirect | Fetch pointer word at direct address; second-level resolution |
| Indexed Indirect | Combine indexing before indirect dereference |
| Extended Memory | If address >= base range, map to extension bank via formula (Appendix F) |
| Stopper / Inactive | Pre-check; raise trap if invalid |

Pipeline function:
```python
resolve_address(raw_addr, flags) -> physical_addr
```
Returns physical address or raises `Trap`.

## 6. Instruction Category Implementation Strategy

### Phase A – Foundational
- Arithmetic: BA, BS, DA, DS, WA, WD, BM, DM, BT, DT.
- Logical: HA, SM, SS, EX.
- Transfer: TX, TS, MT, TN, IT, RT.
- Decision: NA, LA, NN, LN (set branch/sequence actions).
- Shift: SPS, SPE, SWS, SWE, SSL.
- Masked vs Unmasked: apply mask field vs operand flags.
- Print/Peripheral: PRA/PRD/PRO (formatted output), RF/RB/WF/RW (record I/O).
- Control: MPC, PR (state sequencing semantics).
- Simulator: S (mode toggling).
- Checking: CP, CC.

### Phase B – Scientific Option
- Implement floating-point formats, normalization flows.
- Arithmetic ops: FBA/FBS/FDA/FDS & extended/un-normalized variants FBAE, FBSE, FBAU, etc.
- Multiplication/division: FBM/FDM/FBD/FDD.
- Transforms: FFN, FCON, FLN, FNN, ULD, BD, DD.
- Overflow/underflow flags & timing notes (approximate cycle counts if available).

## 7. Peripheral & Print Device Emulation

| Device | Backing |
|--------|---------|
| Tape (RF/RB/WF/RW) | Binary file with record headers & optional rewind pointer |
| Card Reader/Punch | Text file (lines as cards); Punch appends |
| Printer | Output file or stdout channel; format lines from PRA/PRD/PRO |
| Paper Tape | Byte stream file (reader/punch) |
| Random Access Storage | Memory-mapped file blocks |
| Clock (Elapsed/Real-Time) | Wrap Python time; optionally simulated counter |
| Communications Control | Stub for future expansion |

Peripheral dispatch logic:
```python
device = device_registry[paddr]
device.read(...) or device.write(...)
```
Return status or raise device trap on failure.

## 8. Memory Initialization & Loader

Supported formats:
- Raw octal word list.
- Assembler listing (parsing card fields).
- Structured JSON/YAML (addresses to 48‑bit word values).
- Partial overlay loads.

API:
```python
sim.load_image(path, format='auto', base=0)
sim.reset(entry_point=0)
```

## 9. Execution Control API

```python
sim.run(max_instructions=None, breakpoints=None, stop_at=None)
sim.step(count=1)
sim.halt(reason)
sim.resume()
sim.add_breakpoint(address)
sim.remove_breakpoint(address)
```

Breakpoints stored in a set; checked pre-execution.

## 10. Debugging & Introspection

Functions:
- `sim.dump_registers(format='hex')`
- `sim.dump_memory(start, length, radix='octal')`
- `sim.disassemble(start, count)`
- `sim.enable_trace(True/False)`
- Watchpoints: `{address: callback}` on read/write.

CLI Commands (initial):
```
load <path>
run [max]
step [count]
break <addr>
delbreak <addr>
regs
mem <addr> <len>
disas <addr> <count>
devices
attach <type> <path>
detach <id>
trace on|off
halt
save <snapshot_path>
restore <snapshot_path>
```

## 11. Trap & Error Handling

Trap Types:
- Invalid opcode
- Addressing fault (inactive/stopper/barricade)
- Parity error
- Orthocount error
- Overflow/Underflow (scientific)
- Device fault (unattached / I/O error)
- Simulator halt instruction (if defined)
- External stop request

`SimulatorTrap`:
```text
SimulatorTrap {
  code: Enum
  message: str
  context: { pc, mnemonic, raw_word, effective_address? }
}
```
Policy:
- Fatal: halt + record trap.
- Nonfatal (parity if configured): log & continue.

## 12. Timing (Optional Later)

- Maintain `sim.cycles` counter.
- Table mapping mnemonic → cycle count (from Appendix C).
- Enable timing mode flag; if off, skip cycle accumulation.

## 13. Memory Barricade (Appendix G)

Mechanics:
- Barricade register defines protected region.
- Any instruction referencing protected addresses without authorization triggers barricade trap.
- Provide config: `sim.set_barricade(limit)`.

## 14. Multiprogram Control

Later phase:
- Maintain list of active sequence counters.
- Scheduler function rotates among them, or executes one until trap/halt then switches.
- Provide API: `sim.add_program(entry_addr)`, `sim.switch_program(index)`.

## 15. Floating-Point & Scientific Registers

Pending full spec extraction. Plan:
- Define structured representation (sign, exponent, mantissa).
- Utility functions: normalize, add/sub, multiply, divide, detect overflow/underflow.
- Optionally maintain sticky flags.

## 16. State Persistence

Snapshot:
```python
state = sim.export_state()
sim.import_state(state)
```
Serialization to JSON:
- Registers
- Memory (delta encoding for sparse differences)
- Devices status (file offsets)
- Cycle count, trap status

## 17. Testing Plan

### Unit Tests
- Register masking & assignment boundaries.
- Memory read/write + extension mapping.
- Address resolution (direct/indexed/indirect cases).
- Per‑instruction mini-cases (BA, BS, TX, PRA, RF).

### Integration Tests
- Load program performing arithmetic sequences; expected accumulator/product results.
- Peripheral I/O round trip (write then read).
- Printer output lines matching encoded print instruction formatting.

### Scientific Tests
- Floating-point addition, normalization edge, overflow/underflow triggers.

### Regression / Special
- Barricade violation.
- Stopper address halt.
- Trap propagation (parity, orthocount).

### Tooling Tests
- CLI scenario scripts (run -> break -> step -> inspect).
- Snapshot save/restore.

## 18. Incremental Roadmap (Phases & Deliverables)

| Phase | Deliverables |
|-------|--------------|
| 0     | Spec extraction doc (register bit layouts, address forms) |
| 1     | Memory + registers + base decode; simple run/step |
| 2     | Arithmetic/logical/transfer/decision/shift instructions |
| 3     | Peripheral + print devices (file-backed) |
| 4     | Traps (parity, orthocount, barricade), breakpoints, trace |
| 5     | Scientific instruction framework (normalize + subset ops) |
| 6     | Expanded floating-point operations & error flags |
| 7     | Multiprogram sequence counters (optional) |
| 8     | Timing mode + cycle accounting |
| 9     | Snapshot system + CLI polish + documentation |
| 10    | Optimization (pre-decode cache, dispatch speedups) |

## 19. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Missing spec details | Incorrect semantics | Phase 0 spec extraction; annotate assumptions |
| Device complexity | Peripheral errors | Start simple; expand features incrementally |
| Floating-point ambiguity | Incorrect scientific results | Build reference tests from manual examples |
| Performance (Python overhead) | Slow large programs | Pre-decode cache, lightweight dispatch, optional Cython later |
| Trap silence | Hard-to-debug faults | Central trap logger with structured outputs |
| Over-scoped initial phase | Delays | Strict phase boundaries & feature toggles |

## 20. Open Questions (To Resolve in Spec Extraction)

1. Precise width & count of index registers.
2. Exact representation & side effects of sequence counters.
3. Detailed mask index register semantics for masked instructions.
4. Barricade register format & enforcement edge cases.
5. Scientific overflow/underflow flags & recovery behavior.
6. Orthocount definition & algorithmic check logic.
7. Parity calculation domain (instruction word vs data word).
8. Handling of “inactive” addresses beyond simple traps (ignore vs halt).
9. Memory packing (are multiple 12‑bit instructions stored per 48‑bit word or each word holds a single instruction?).

## 21. Immediate Action Items

- [x] Create `docs/h1800-spec.md` with extracted register & addressing bit definitions.
- [ ] Scaffolding: `h1800/` directory skeleton (cpu, memory, registers, decoder, executor, devices, sim, cli).
- [ ] Port opcode metadata into a neutral structure reused by decoder & executor.
- [ ] Implement memory + register classes (with 48‑bit masking).
- [ ] Basic decode + run loop; support BA and TX to validate control flow.
- [ ] Simple printer device & test PRA output stub.
- [ ] Draft initial CLI tool with `load`, `step`, `run`, `regs`, `mem`.

## 22. Style & Implementation Guidelines

- Pure Python first; type hints throughout.
- Mask integers on write (`value & ((1<<48)-1)` for data words).
- Avoid premature micro-optimizations; add profiling hooks after correctness.
- Use dataclasses for structured state objects (Instruction, CPUState, SimulatorState).
- Logging: optional structured trace lines (CSV or JSON); off by default.
- Clear separation of decode vs execute to enable pre-decode caching.
- Device operations raise specific `DeviceError` mapped to `SimulatorTrap`.

## 23. Extension & Future Work

- Graphical/TUI debugger (memory/register panes).
- Networked peripheral simulation (communications control).
- Macro-level performance profiling; histograms of instruction usage.
- Formal verification harness for arithmetic edge cases.
- Remote control API (REST/WebSocket) for integration with external tools.

---

## 24. Summary

This plan decomposes the Honeywell 1800 simulator into clean, testable layers with a phased roadmap ensuring early functionality (basic instructions and control) precedes advanced features (scientific ops, multiprogram control, timing). The design emphasizes modularity (devices, executor dispatch), debuggability (trace, breakpoints, watchpoints), and extensibility (snapshots, peripheral expansion). By locking down the specification details first, implementation can progress confidently without semantic drift.

---

*End of Document.*
