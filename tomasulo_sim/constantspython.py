DEFAULT_CONFIG = {

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