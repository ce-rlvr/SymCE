import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.ntheory import factorint

# Named object bindings for rings (integers represent Z/nZ, 0 represents Z)
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = True
        elif witness in [ZZ, QQ, RR, CC, S.Integers, S.Reals, S.Complexes, S.Rationals]:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h2 = True
        elif witness in [ZZ, QQ, RR, CC, S.Integers, S.Reals, S.Complexes, S.Rationals]:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: R is NOT a local ring
    try:
        if isinstance(witness, (int, sympy.Integer)):
            w = abs(int(witness))
            if w == 0:
                is_local = False
            elif w == 1:
                is_local = False
            else:
                factors = factorint(w)
                is_local = (len(factors) == 1)
        elif witness in [QQ, RR, CC, S.Reals, S.Complexes, S.Rationals]:
            is_local = True
        elif witness in [ZZ, S.Integers]:
            is_local = False
        else:
            # Default to True for unknown rings so neg_Q becomes False (rejects invalid witnesses)
            is_local = True
            
        neg_q = not is_local
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2