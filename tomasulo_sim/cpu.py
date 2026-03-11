from logging import config

from reservation_station import RSEntry
from constantspython import *
from instruction import Instruction
"""
cpu.py

This file implements the main TomasuloCPU simulator for the project. The CPU models a dynamically 
scheduled processor that executes a subset of RISC-V
instructions using Tomasulo’s algorithm. The simulator includes reservation stations, a register alias
table for register renaming,and a single commondata bus for result forwarding.

Each cycle of the simulation performs the stages of writeback, execute, issue, and fetch. Instructions are issued to reservation stations when
available and execute once their operands are ready. Results are broadcast on the common data bus so dependent instructions can receive forwarded
values immediately.

The simulator tracks execution cycles, structural stalls, register values,
and memory state to verify functional and timing correctness of the architecture.
"""
class TomasuloCPU:

    def __init__(self, memory, program, labels, config):

        self.memory = memory
        self.program = program
        self.labels = labels
        self.debug = False #used temporarily for testing 

        self.int_regs = {f"R{i}":0 for i in range(32)}
        self.fp_regs = {f"F{i}":0.0 for i in range(32)}

        self.rat = {**{f"R{i}":None for i in range(32)},
                    **{f"F{i}":None for i in range(32)}}

        self.pc = 0
        self.cycle = 0
        self.decode_buffer = []
        self.fetch_stall = False

        self.issue_counter = 1
        self.stall_events = 0
        self.NI = config["NI"]
        rs_cfg = config["RS"]
        self.rs = {
            unit: [RSEntry(f"{unit}{i}", unit) for i in range(count)]
            for unit, count in rs_cfg.items()
        }

    def reg_read(self, reg):
        if reg == "R0":
            return 0
        if reg.startswith("R"):
            return self.int_regs[reg]
        return self.fp_regs[reg]

    def reg_write(self, reg,val):
        if reg == "R0":
            return
        if reg.startswith("R"):
            self.int_regs[reg]=int(val)
        else:
            self.fp_regs[reg]=float(val)
    def fetch(self):

        if len(self.decode_buffer) >= self.NI:
            return

        if self.fetch_stall:
            return

        if self.pc >= len(self.program):
            return

        inst = self.program[self.pc]

        self.decode_buffer.append(inst)
        self.pc += 1

        if inst.op == "bne":
            self.fetch_stall = True

    def get_free_rs(self,unit):

        for r in self.rs[unit]:
            if not r.busy:
                return r
        return None

    def issue(self):

        if not self.decode_buffer:
            return

        inst = self.decode_buffer[0]
        unit = UNIT_FOR_OP[inst.op]

        rs = self.get_free_rs(unit)

        if not rs:
            self.stall_events += 1
            return

        rs.busy = True
        rs.op = inst.op
        rs.instr = inst
        rs.issue_id = self.issue_counter
        self.issue_counter += 1

        if inst.op == "add":

            self.set_operand(rs, "j", inst.rs1)
            self.set_operand(rs, "k", inst.rs2)

            rs.dest = inst.rd
            self.rat[inst.rd] = rs.name
        
        elif inst.op == "addi":

            self.set_operand(rs, "j", inst.rs1)

            rs.Vk = inst.imm
            rs.Qk = None

            rs.dest = inst.rd
            self.rat[inst.rd] = rs.name

        elif inst.op == "fsd":

            # base register
            self.set_operand(rs,"j",inst.rs2)

            # value to store
            self.set_operand(rs,"k",inst.rs1)

        elif inst.op == "fld":

            self.set_operand(rs,"j",inst.rs1)

            rs.Vk = inst.imm
            rs.Qk = None

            rs.dest = inst.rd
            self.rat[inst.rd] = rs.name
        elif inst.op == "bne":

            self.set_operand(rs,"j",inst.rs1)
            self.set_operand(rs,"k",inst.rs2)

            rs.target_pc = self.labels[inst.label]

        elif inst.op in ("fadd","fmul","fdiv"):

            self.set_operand(rs,"j",inst.rs1)
            self.set_operand(rs,"k",inst.rs2)

            rs.dest = inst.rd
            self.rat[inst.rd] = rs.name

        else:

            if inst.rs1:
                tag = self.rat[inst.rs1]
                if tag:
                    rs.Qj = tag
                else:
                    rs.Vj = self.reg_read(inst.rs1)

            if inst.rs2:
                tag = self.rat[inst.rs2]
                if tag:
                    rs.Qk = tag
                else:
                    rs.Vk = self.reg_read(inst.rs2)
        self.debug_events["issued"] = f"{rs.name} <= {inst.raw}"
        self.decode_buffer.pop(0)

    def set_operand(self, rs, which, reg):

        tag = self.rat[reg]
        if tag:
            if which == "j":
                rs.Qj = tag
            else:
                rs.Qk = tag
        else:
            value = self.reg_read(reg)

            if which == "j":
                rs.Vj = value
            else:
                rs.Vk = value
    def execute(self):

        for unit in self.rs.values():
            for rs in unit:

                if rs.busy and not rs.executing and not rs.finished_exec:
                    if rs.Qj is None and rs.Qk is None:
                        rs.executing = True
                        rs.remaining = LATENCY[rs.unit_type]
                        self.debug_events["started_exec"].append(f"{rs.name} {rs.op}")

                if rs.executing:
                    rs.remaining -= 1

                    if rs.remaining == 0:
                        rs.executing = False
                        rs.finished_exec = True
                        self.compute_result(rs)
                        self.debug_events["finished_exec"].append(f"{rs.name} {rs.op}")

    def compute_result(self,rs):

        op=rs.op

        if op=="add":
            rs.result=rs.Vj+rs.Vk

        if op=="addi":
            rs.result=rs.Vj+rs.instr.imm

        if op=="fadd":
            rs.result=rs.Vj+rs.Vk

        if op=="fmul":
            rs.result=rs.Vj*rs.Vk

        if op=="fdiv":
            rs.result=rs.Vj/rs.Vk

        if op=="fld":
            addr=rs.Vj+rs.instr.imm
            rs.result=self.memory.get(addr,0)

        if op == "fsd":
            addr = rs.Vj + rs.instr.imm
            rs.addr = int(addr)
            rs.store_val = rs.Vk

        if op=="bne":
            rs.result=(rs.Vj!=rs.Vk)

    def writeback(self):

        ready = []

        for pool in self.rs.values():
            for rs in pool:
                if rs.busy and rs.finished_exec:
                    ready.append(rs)

        if not ready:
            return

        ready.sort(key=lambda x: x.issue_id)
        rs = ready[0]

        self.debug_events["writeback"] = f"{rs.name} {rs.op}"

        if rs.op == "fsd":
            self.memory[rs.addr] = rs.store_val
            self.debug_events["writeback"] += f" -> MEM[{rs.addr}] = {rs.store_val}"
            rs.clear()
            return

        if rs.op == "bne":
            taken = bool(rs.result)
            if taken:
                self.pc = rs.target_pc
            self.fetch_stall = False
            self.debug_events["branch"] = f"bne {'TAKEN' if taken else 'NOT TAKEN'}"
            rs.clear()
            return

        tag = rs.name
        value = rs.result

        for pool in self.rs.values():
            for r in pool:
                if r.Qj == tag:
                    r.Qj = None
                    r.Vj = value
                if r.Qk == tag:
                    r.Qk = None
                    r.Vk = value

        if rs.dest and self.rat[rs.dest] == tag:
            self.reg_write(rs.dest, value)
            self.rat[rs.dest] = None

        self.debug_events["writeback"] += f" -> {rs.dest} = {value}"
        rs.clear()

    def done(self):

        if self.pc < len(self.program):
            return False

        if self.decode_buffer:
            return False

        for pool in self.rs.values():
            for rs in pool:
                if rs.busy:
                    return False

        return True

    # def step(self):

    #     self.cycle+=1

    #     self.writeback()
    #     self.execute()
    #     self.issue()
    #     self.fetch()
    def step(self):
        self.cycle += 1

        self.debug_events = {
            "writeback": None,
            "issued": None,
            "started_exec": [],
            "finished_exec": [],
            "branch": None,
        }

        self.writeback()
        self.execute()
        self.issue()
        self.fetch()

        if self.debug:
            self.print_cycle_trace()

    def print_cycle_trace(self):
        print(f"\n===== Cycle {self.cycle} =====")
        print(f"PC: {self.pc}")
        print(f"Decode Buffer: {self.decode_buffer.raw if self.decode_buffer else 'Empty'}")
        print(f"Fetch Stall: {self.fetch_stall}")

        if self.debug_events["issued"]:
            print(f"Issued: {self.debug_events['issued']}")
        if self.debug_events["started_exec"]:
            print("Started Exec:", ", ".join(self.debug_events["started_exec"]))
        if self.debug_events["finished_exec"]:
            print("Finished Exec:", ", ".join(self.debug_events["finished_exec"]))
        if self.debug_events["writeback"]:
            print(f"Writeback: {self.debug_events['writeback']}")
        if self.debug_events["branch"]:
            print(f"Branch: {self.debug_events['branch']}")

        print("Busy RS:")
        any_busy = False
        for unit_name, pool in self.rs.items():
            for rs in pool:
                if rs.busy:
                    any_busy = True
                    print(
                        f"  {rs.name}: op={rs.op}, "
                        f"Vj={rs.Vj}, Vk={rs.Vk}, "
                        f"Qj={rs.Qj}, Qk={rs.Qk}, "
                        f"dest={rs.dest}, exec={rs.executing}, "
                        f"rem={rs.remaining}, done={rs.finished_exec}, "
                        f"issue_id={rs.issue_id}"
                    )
        if not any_busy:
            print("  None")

    def run(self):

        while not self.done():
            self.step()