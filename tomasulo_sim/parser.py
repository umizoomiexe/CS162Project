import re
from instruction import Instruction
"""
parses the input  file

The input file contains memory initialization values and RISC-V assembly instructions

The parser extracts the initial memory contents, instructions and branch labels

Returned to the CPU simulator for execution
"""


def parse_file(filename):

    memory = {}
    program = []
    labels = {}

    with open(filename) as f:
        lines = [l.strip() for l in f if l.strip()]

    program_lines = []

    for line in lines:
        if line.startswith("%"):
            continue

        if re.match(r"^-?\d+\s*,\s*-?\d+", line):
            addr, val = line.split(",")
            memory[int(addr)] = float(val)
        else:
            program_lines.append(line)

    pc = 0
    for line in program_lines:
        if ":" in line:
            label, rest = line.split(":")
            labels[label.strip()] = pc
            if rest.strip():
                pc += 1
        else:
            pc += 1

    for line in program_lines:
        if ":" in line:
            _, line = line.split(":")
            line = line.strip()
            if not line:
                continue

        program.append(parse_instruction(line))

    return memory, program, labels


def parse_instruction(line):

    tokens = line.replace(",", " ").split()
    op = tokens[0]

    if op == "add":
        return Instruction(op, tokens[1], tokens[2], tokens[3], raw=line)

    if op == "addi":
        return Instruction(op, tokens[1], tokens[2], imm=int(tokens[3]), raw=line)

    if op in ("fadd", "fmul", "fdiv"):
        return Instruction(op, tokens[1], tokens[2], tokens[3], raw=line)

    if op in ("fld", "fsd"):
        reg = tokens[1]
        m = re.match(r"(-?\d+)\((R\d+)\)", tokens[2])
        imm = int(m.group(1))
        base = m.group(2)

        if op == "fld":
            return Instruction(op, rd=reg, rs1=base, imm=imm, raw=line)

        return Instruction(op, rs1=reg, rs2=base, imm=imm, raw=line)

    if op == "bne":
        return Instruction(op, rs1=tokens[1], rs2=tokens[2].replace("$0","R0"), label=tokens[3], raw=line)

    raise ValueError("Unknown instruction")