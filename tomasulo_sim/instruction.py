"""
instruction.py

Defines the Instruction data structure used by the Tomasulo simulator.

Each instruction parsed from the input assembly program is stored as an
Instruction object. The fields store the decoded components of the
instruction so they can be used by the CPU simulator.
"""

from dataclasses import dataclass
from typing import Optional

"""
single decoded RISC-V instruction:
op  opcode of the instruction
rd  destination register
rs1 source register 1
rs2 source register 2
imm    immediate value (used for addi, loads/stores)
label  branch target label (for bne)
raw    original text representation of the instruction
"""

@dataclass
class Instruction:
    op: str
    rd: Optional[str] = None
    rs1: Optional[str] = None
    rs2: Optional[str] = None
    imm: Optional[int] = None
    label: Optional[str] = None
    raw: str = ""