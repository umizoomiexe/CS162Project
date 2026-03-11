"""
constantspython.py

defines the architectural configuration parameters used by the Tomasulo CPU simulator

Includes Default architectural configuration, Functional unit latencies, Mapping between instructions and functional units

These parameters allow the simulator to easily be reconfigured for the
bonus experiments (changing instruction queue size or reservation stations)
"""


# Default architecture configuration used by the simulator
DEFAULT_CONFIG = {


    # NI = Instruction queue (decode buffer) size
    # The base architecture specifies NI = 1
    "NI": 1,

    "RS": {
        "INT": 4,
        "LS": 3,
        "FPADD": 3,
        "FPMUL": 2,
        "FPDIV": 1,
        "BU": 1
    }
}
# Latency (in cycles) for each functional unit
# These values come directly from the project specification

LATENCY = {
    "INT": 1,
    "LS": 2,
    "FPADD": 3,
    "FPMUL": 4,
    "FPDIV": 6,
    "BU": 1
}

# Mapping from instruction opcode to the functional unit type
# Used when issuing instructions to determine which reservation station pool
# should be used.

UNIT_FOR_OP = {
    "add": "INT",
    "addi": "INT",
    "fld": "LS",
    "fsd": "LS",
    "fadd": "FPADD",
    "fmul": "FPMUL",
    "fdiv": "FPDIV",
    "bne": "BU"
}