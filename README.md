# Tomasulo OoO CPU Simulator

This project implements a functional and timing simulator for a simplified out-of-order CPU using Tomasulo’s Algorithm. The simulator models a non-speculative, single-issue processor without a Reorder Buffer (ROB), using reservation stations, a register status table for implicit renaming, and a single Common Data Bus (CDB). The simulator supports a subset of the RISC-V ISA and executes an input assembly program cycle by cycle. The project follows the CS 162 course project specification and lab guidance. :contentReference[oaicite:0]{index=0} :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}

## Supported Instructions

The simulator supports the following 8 instructions:

- `fld`
- `fsd`
- `add`
- `addi`
- `fadd`
- `fmul`
- `fdiv`
- `bne` :contentReference[oaicite:3]{index=3}

## Simulated Architecture

The CPU model is a non-speculative, single-issue, out-of-order processor with the following pipeline structure:

- Fetch (`NF = 1`)
- Decode buffer (`NI = 1`)
- Issue (`NW = 1`)
- Execute
- Write Result / CDB (`NB = 1`) :contentReference[oaicite:4]{index=4}

### Functional Units

| Unit | Latency | Reservation Stations | Instructions |
|------|---------|----------------------|--------------|
| INT | 1 | 4 | `add`, `addi` |
| Load/Store | 2 | 3 | `fld`, `fsd` |
| FPadd | 3 | 3 | `fadd` |
| FPmult | 4 | 2 | `fmul` |
| FPdiv | 6 | 1 | `fdiv` |
| BU | 1 | 1 | `bne` |

These parameters follow the project and lab specification. :contentReference[oaicite:5]{index=5} :contentReference[oaicite:6]{index=6}

## Main Features

- Single-issue Tomasulo scheduling
- Reservation stations for all functional units
- Register status table (RAT/Register Result Status) for implicit renaming
- No ROB
- One CDB with oldest-issued instruction priority on contention
- Forwarding through the CDB
- Branch handling with no prediction
- Cycle-by-cycle timing simulation
- Final register and memory dump
- Total cycle count and issue-stage structural stall count

The project specification requires functional correctness, timing correctness, and stall tracking. :contentReference[oaicite:7]{index=7}

## Project Files

- `sim.py`  
  Main entry point. Parses command-line arguments, loads the program, creates the CPU, runs the simulation, and prints results.

- `cpu.py`  
  Contains the main Tomasulo simulator logic, including fetch, issue, execute, writeback, branch handling, CDB arbitration, and cycle stepping.

- `parser.py`  
  Parses the input file into memory initialization, instruction list, and label table.

- `instruction.py`  
  Defines the `Instruction` data structure.

- `reservation_station.py`  
  Defines the reservation station entry data structure.

- `constants.py`  
  Stores architecture constants such as latencies, reservation station counts, and instruction-to-unit mappings.

## Requirements

- Python 3.10 or newer recommended
- No external libraries are required

## How to Run

Run the simulator from the project directory with:

```bash
python sim.py <input_file>