# ItsyBitsy CPU

A custom 8-bit CPU designed and simulated in **Logisim-Evolution**, complete with a hand-rolled assembler that compiles a purpose-built assembly language (*HOHOHO*) into Logisim-compatible RAM image files.

Built by **Aaditya Kulkarni** and **Samdarshi Kumar Rai** — presented by *RacingBits Corporation*.

---

## Overview

ItsyBitsy is a single-cycle, non-pipelined 8-bit CPU featuring:

- 4 general-purpose 8-bit registers (`X0`–`X3`)
- An ALU supporting addition and multiplication
- Two RAM modules (instruction fetch + memory access/writeback)
- A Python assembler that translates `.text`/`.data` programs into Logisim hex image files

---

## Repository Contents

| File | Description |
|---|---|
| `ItsyBitsy.circ` | Logisim-Evolution circuit file containing the full CPU |
| `ItsyBitsyAssembler_EC.py` | Python assembler — converts assembly programs to Logisim hex images |
| `Sample_program.txt` | Example program demonstrating all 4 instructions and all registers |
| `text_output.hex` | Assembled instruction memory image (output of assembler) |
| `data_output.hex` | Assembled data memory image (output of assembler) |
| `ItsyBitsy_UserManual_EC.pdf` | Full user manual including architecture, ISA, and usage guide |

---

## Architecture

### Register File
Four general-purpose 8-bit registers: `X0`, `X1`, `X2`, `X3`. Each supports synchronous writes via the global clock and a `WriteEnable` signal.

### ALU
Takes operands from the register file via a multiplexer and supports:
- 8-bit **addition**
- 8-bit **multiplication**

A multiplexer selects the output based on the decoded instruction opcode.

### Memory
Two RAM modules, both with 8-bit data width:
- **Instruction Fetch RAM** — loaded with `text_output.hex`
- **Memory Access / Writeback RAM** — loaded with `data_output.hex`

Memory addressing is provided directly by register outputs.

### Datapath Summary
```
[Instruction Fetch RAM] → [Decoder] → [Register File] → [ALU] → [Writeback / Memory RAM]
```
Single-cycle execution. One instruction completes per clock edge.

---

## Instruction Set (HOHOHO)

All instructions follow the same 3-register format: `INSTR Rd, Rn, Rm`

### Encoding — 8-bit instruction word

| Bits [7:6] | Bits [5:4] | Bits [3:2] | Bits [1:0] |
|---|---|---|---|
| Opcode | Rd | Rn | Rm |

### Opcode Map

| Instruction | Opcode | Operation |
|---|---|---|
| `STORE` | `00` | `M[Rn, Rm] = Rd` |
| `PLUS` | `01` | `Rd = Rn + Rm` |
| `CROSS` | `10` | `Rd = Rn * Rm` |
| `LOAD` | `11` | `Rd = M[Rn, Rm]` |

### Register Map

| Register | Encoding |
|---|---|
| `X0` | `00` |
| `X1` | `01` |
| `X2` | `10` |
| `X3` | `11` |

### Instruction Reference

**`PLUS Rd, Rn, Rm`** — Addition
```
Rd = Rn + Rm
```

**`CROSS Rd, Rn, Rm`** — Multiplication
```
Rd = Rn * Rm
```

**`LOAD Rd, Rn, Rm`** — Load from memory
```
Rd = M[Rn, Rm]    # Rn = base address, Rm = byte offset
```

**`STORE Rd, Rn, Rm`** — Store to memory
```
M[Rn, Rm] = Rd    # Rn = base address, Rm = byte offset
```

> **Note:** All register values are assumed to be non-negative integers. Immediate values are not supported.

---

## Assembler

`ItsyBitsyAssembler_EC.py` is a pure Python assembler that parses `.text` and `.data` sections and produces two Logisim-compatible hex image files.

### How it works

1. Reads an assembly program file with `.text` and `.data` sections
2. Parses each instruction, validates registers and opcodes, encodes to 8-bit binary
3. Pads both outputs to 256 bytes
4. Writes `text_output.hex` and `data_output.hex` in Logisim v3.0 hex format

### Syntax rules

- Comments use `#` or `//`
- Commas between operands are optional — all of these are valid:
  ```
  PLUS X0, X1, X2
  PLUS X0 X1 X2
  PLUS X0 ,X1,  X2
  ```
- Instructions are case-insensitive
- Blank lines and comment-only lines are ignored
- `.data` values must be integers in range `0–255`

### Running the assembler

```bash
python ItsyBitsyAssembler_EC.py
```

By default it assembles `Sample_program.txt` and writes `text_output.hex` and `data_output.hex`. To assemble a different file, edit the call at the bottom of the script:

```python
assemble_file("your_program.txt")
# or with custom output filenames:
assemble_file("your_program.txt", text_out="my_text.hex", data_out="my_data.hex")
```

> **Tip:** Keep your program file, the assembler, and the `.circ` file in the same folder. The assembler uses relative paths and will raise a `FileNotFoundError` if they are separated.

---

## Usage — Running a Program

### Step 1 — Write your program

Create a `.txt` file with `.text` and `.data` sections:

```
.text
PLUS  X2, X1, X2     # X2 = X1 + X2
CROSS X1, X0, X3     # X1 = X0 * X3
LOAD  X2, X3, X1     # X2 = M[X3, X1]
STORE X3, X1, X0     # M[X1, X0] = X3

.data
0
1
42
```

If you have no data values, still include:
```
.data
0
```

### Step 2 — Assemble

Run the assembler to produce `text_output.hex` and `data_output.hex`.

### Step 3 — Open the circuit

1. Install [Logisim-Evolution 4.0.0](https://github.com/logisim-evolution/logisim-evolution) or later
2. Open `ItsyBitsy.circ` via **File → Open**

### Step 4 — Load the image files

- Find the **Instruction Fetching** section (bottom-left of the circuit)
- Right-click the RAM → **Load Image** → select `text_output.hex`
- Find the **Memory Access / Writeback** RAM
- Right-click → **Load Image** → select `data_output.hex`

### Step 5 — Set register values

Using the finger-pointer tool in Logisim, click each register involved in your first instruction and enter the desired initial values manually.

### Step 6 — Run

- **Manual stepping:** Simulate → Tick Once (or keyboard shortcut)
- **Continuous:** Simulate → Auto-Tick Enabled, then toggle the clock

The clock component is in the upper-left of the circuit.

---

## Sample Program

```
.text
# Demonstrates all 4 instructions, all registers, and flexible spacing

PLUS  X2, X1, X2        # X2 = X1 + X2
CROSS X1, X0, X3        # X1 = X0 * X3
LOAD  X2, X3, X1        # X2 = M[X3, X1]
CROSS X0, X2, X1        # X0 = X2 * X1
PLUS  X3  X2  X1        # X3 = X2 + X1
STORE X3  X1  X0        # M[X1, X0] = X3
PLUS  X2 , X2  X0       # X2 = X2 + X0
CROSS X0 ,X1,  X3       # X0 = X1 * X3
STORE X0, X2 , X0       # M[X2, X0] = X0

.data
0
1
2
34
5
6
```

**Assembled output (`text_output.hex`, first 9 bytes):**
```
66 93 ed 89 79 34 68 87 08
```

---

## Encoding Example

`PLUS X2, X1, X2` encodes as:

| Field | Value | Bits |
|---|---|---|
| Opcode (PLUS) | `01` | [7:6] |
| Rd (X2) | `10` | [5:4] |
| Rn (X1) | `01` | [3:2] |
| Rm (X2) | `10` | [1:0] |

Binary: `01100110` → Hex: **`0x66`** ✓ (matches first byte of output)

---

## Requirements

| Tool | Version |
|---|---|
| Python | 3.x (no external libraries required) |
| Logisim-Evolution | 4.0.0 or later |

---

## Authors

| Name | Contribution |
|---|---|
| **Aaditya Kulkarni** | Datapath architecture, register file, ALU subsystem, multiplexer routing, arithmetic components, assembler script, documentation |
| **Samdarshi Kumar Rai** | Memory components, RAM control logic, decoder circuits, write-enable management, debugging and verification, documentation |

*Opcode design and assembler architecture were a joint contribution.*

---

## Course

CS 382 — Computer Architecture  
Stevens Institute of Technology
