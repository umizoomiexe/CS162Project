from dataclasses import dataclass
from typing import Optional


@dataclass
class Instruction:
    op: str
    rd: Optional[str] = None
    rs1: Optional[str] = None
    rs2: Optional[str] = None
    imm: Optional[int] = None
    label: Optional[str] = None
    raw: str = ""