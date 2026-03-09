INT_RS = 4
LS_RS = 3
FPADD_RS = 3
FPMUL_RS = 2
FPDIV_RS = 1
BU_RS = 1

LATENCY = {
    "INT": 1,
    "LS": 2,
    "FPADD": 3,
    "FPMUL": 4,
    "FPDIV": 6,
    "BU": 1
}

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