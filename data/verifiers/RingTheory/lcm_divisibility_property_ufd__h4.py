import sympy
from sympy.abc import x, y, z

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                _, a, b, c = witness
            elif len(witness) == 3:
                a, b, c = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        # We evaluate in the domain of integers (Z), which is a UFD.
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(c, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        if not h2:
            h3 = False
        elif a == 0:
            h3 = (c == 0)
        else:
            h3 = (c % a == 0)
    except Exception:
        h3 = False

    try:
        if not h2:
            neg_q = False
        else:
            l = sympy.lcm(a, b)
            if l == 0:
                neg_q = (c != 0)
            else:
                neg_q = (c % l != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are elements of R",
    "H_3: a divides c",
    "¬Q: lcm(a, b) does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3