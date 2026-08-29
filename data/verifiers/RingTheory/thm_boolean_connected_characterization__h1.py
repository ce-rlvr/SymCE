import sympy

Z = sympy.ZZ
Q = sympy.QQ
R = sympy.RR
C = sympy.CC
ZZ = sympy.ZZ
QQ = sympy.QQ

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10

KNOWN_DOMAINS = [
    sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC,
    sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes
]

def conditions(witness) -> list[bool]:
    # H_1: R has an identity element 1 != 0
    try:
        if isinstance(witness, int) and witness >= 2:
            h1 = True
        elif witness in KNOWN_DOMAINS:
            h1 = True
        elif type(witness).__name__ == 'GaloisField':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: The only idempotent elements in R are 0 and 1
    try:
        if isinstance(witness, int) and witness >= 2:
            idemps = [x for x in range(witness) if (x * x) % witness == x]
            h2 = (set(idemps) == {0, 1})
        elif witness in KNOWN_DOMAINS:
            h2 = True
        elif type(witness).__name__ == 'GaloisField':
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is not isomorphic to Z_2
    try:
        if isinstance(witness, int) and witness >= 2:
            is_z2 = (witness == 2)
        elif witness in KNOWN_DOMAINS:
            is_z2 = False
        elif type(witness).__name__ == 'GaloisField':
            is_z2 = (witness.mod == 2)
        else:
            is_z2 = False
        neg_q = not is_z2
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R has an identity element 1 != 0",
    "H_2: The only idempotent elements in R are 0 and 1",
    "¬Q: R is not isomorphic to Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2