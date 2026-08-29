import sympy
from sympy import ZZ, QQ
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        if witness == ZZ:
            return [True]
        if witness == QQ:
            return [False]
    except Exception:
        pass

    try:
        n = int(witness)
        if n == 0:
            return [True]
        if n == 1:
            return [True]
        if n > 1:
            factors = factorint(n)
            is_local = (len(factors) == 1)
            return [not is_local]
    except Exception:
        pass

    return [False]

CONDITION_LABELS = ["neg_Q: R modulo x**2 is not a local ring"]
N_HYP = 0
NEG_Q_INDEX = 0