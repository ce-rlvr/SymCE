import math
from sympy import ZZ, QQ

class CustomRing:
    def __init__(self, is_commutative=True, is_local=True, krull_dimension=0):
        self.is_commutative = is_commutative
        self.is_local = is_local
        self.krull_dimension = krull_dimension

# Predefined objects that might be used as witnesses
R_inf = CustomRing(is_commutative=True, is_local=True, krull_dimension=math.inf)
R_noeth = CustomRing(is_commutative=True, is_local=True, krull_dimension=1)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, str):
            s = witness.lower()
            if "..." in s or "inf" in s:
                is_loc = "local" in s or "_m" in s or "_{m}" in s or "m" in s
                return [True, is_loc, True]
            elif s == "z" or "integer" in s:
                return [True, False, False]
            elif s == "q" or s == "r" or s == "c" or "field" in s:
                return [True, True, False]
    except Exception:
        pass

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            neg_q = (witness[2] == math.inf or witness[2] == float('inf'))
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_Field') and witness.is_Field:
            return [True, True, False]
    except Exception:
        pass

    try:
        h1 = bool(witness.is_commutative)
    except Exception:
        pass

    try:
        h2 = bool(witness.is_local)
    except Exception:
        pass

    try:
        kd = witness.krull_dimension
        neg_q = (kd == math.inf or kd == float('inf'))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with a unique maximal ideal",
    "¬Q: The Krull dimension of R is infinite"
]

N_HYP = 2
NEG_Q_INDEX = 2