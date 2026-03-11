import sys
from parser import parse_file
from cpu import TomasuloCPU
from constantspython import DEFAULT_CONFIG

def print_results(cpu):

    print("\n==============================")
    print("SIMULATION RESULTS")
    print("==============================")

    print(f"\nTotal Execution Cycles : {cpu.cycle}")
    print(f"Issue Stall Events     : {cpu.stall_events}")

    print("\n------------------------------")
    print("Integer Registers")
    print("------------------------------")

    for i in range(32):
        reg = f"R{i}"
        print(f"{reg:>4} : {cpu.int_regs[reg]}")

    print("\n------------------------------")
    print("Floating Point Registers")
    print("------------------------------")

    for i in range(32):
        reg = f"F{i}"
        print(f"{reg:>4} : {cpu.fp_regs[reg]}")

    print("\n------------------------------")
    print("Memory (Non-Zero Entries)")
    print("------------------------------")

    for addr in sorted(cpu.memory):
        val = cpu.memory[addr]
        print(f"[{int(addr):>4}] : {val}")

    print()

def run_experiment(memory, program, labels, config):

    cpu = TomasuloCPU(memory.copy(), program, labels, config)
    cpu.run()

    return cpu.cycle

def main():

    if len(sys.argv)!=2:
        print("Usage: python sim.py program.dat")
        return

    memory, program, labels = parse_file(sys.argv[1])

    config = DEFAULT_CONFIG

    cpu = TomasuloCPU(memory, program, labels, config)
    cpu.debug = False # swicth to true when wanting to se trace of each cycle for testing
    cpu.run()

    print_results(cpu)
    print("\n==============================")
    print("BONUS EXPERIMENTS")
    print("==============================")

    # Test different NI sizes
    for ni in [1, 4, 16]:

        config_test = {
            "NI": ni,
            "RS": DEFAULT_CONFIG["RS"]
        }

        cycles = run_experiment(memory, program, labels, config_test)

        print(f"NI = {ni} → {cycles} cycles")


    # Test smaller RS configuration
    small_rs = {
        "INT":2,
        "LS":2,
        "FPADD":2,
        "FPMUL":2,
        "FPDIV":2,
        "BU":1
    }

    config_test = {
        "NI":1,
        "RS":small_rs
    }

    cycles = run_experiment(memory, program, labels, config_test)

    print(f"RS size = 2 each → {cycles} cycles")

if __name__ == "__main__":
    main()