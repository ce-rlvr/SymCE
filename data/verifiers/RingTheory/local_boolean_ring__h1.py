import sympy
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n <= 1:
                h1 = False
            else:
                # Z/nZ is a local ring iff n is a prime power
                h1 = len(factorint(n)) == 1
        elif witness in (QQ, RR, CC):
            h1 = True
        elif witness == ZZ:
            h1 = False
        elif type(witness).__name__ == 'FiniteField':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            neg_q = (n != 2)
        elif type(witness).__name__ == 'FiniteField':
            neg_q = (witness.mod != 2)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1