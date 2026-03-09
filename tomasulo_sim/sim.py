import sys
from parser import parse_file
from cpu import TomasuloCPU


def main():

    if len(sys.argv)!=2:
        print("Usage: python sim.py program.dat")
        return

    memory, program, labels = parse_file(sys.argv[1])

    cpu = TomasuloCPU(memory, program, labels)
    cpu.debug = False # swicth to true when wanting to se trace of each cycle for testing
    cpu.run()

    print("Total Cycles:", cpu.cycle)
    print("Stall Events:", cpu.stall_events)

    print("\nRegisters")

    for r,v in cpu.int_regs.items():
        print(r,v)

    for r,v in cpu.fp_regs.items():
        print(r,v)

    print("\nMemory")

    for addr,val in sorted(cpu.memory.items()):
        print(addr,val)


if __name__ == "__main__":
    main()