from dataclasses import dataclass
from typing import Optional
from instruction import Instruction


@dataclass
class RSEntry:
    name: str
    unit_type: str
    busy: bool = False

    op: Optional[str] = None
    Vj: Optional[float] = None
    Vk: Optional[float] = None
    Qj: Optional[str] = None
    Qk: Optional[str] = None

    dest: Optional[str] = None
    instr: Optional[Instruction] = None

    issue_id: Optional[int] = None
    executing: bool = False
    remaining: Optional[int] = None
    finished_exec: bool = False

    result: Optional[float] = None
    addr: Optional[int] = None
    store_val: Optional[float] = None
    target_pc: Optional[int] = None

    def clear(self):
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.dest = None
        self.instr = None
        self.issue_id = None
        self.executing = False
        self.remaining = None
        self.finished_exec = False
        self.result = None
        self.addr = None
        self.store_val = None
        self.target_pc = None