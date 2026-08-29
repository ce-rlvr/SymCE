import sympy
from sympy import S, ZZ, QQ, RR, CC
from sympy.abc import x, y, z
import math
import itertools
import functools

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: M is a maximal ideal of R",
    "H_3: n is a positive integer",
    "¬Q: P is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            n = witness.get('n')
            P = witness.get('P')
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            R, M, n, P = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if R in ("ZZ", "Z", S.Integers, ZZ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
    except Exception:
        h1 = False

    # H_2: M is a maximal ideal of R
    try:
        h2 = False
        if R in ("ZZ", "Z", S.Integers, ZZ):
            if isinstance(M, (int, sympy.Integer)):
                h2 = sympy.isprime(abs(M))
            elif isinstance(M, (list, tuple, set)) and len(M) == 1:
                gen = list(M)[0]
                if isinstance(gen, (int, sympy.Integer)):
                    h2 = sympy.isprime(abs(gen))
    except Exception:
        h2 = False

    # H_3: n is a positive integer
    try:
        h3 = False
        if isinstance(n, (int, sympy.Integer)):
            h3 = (n > 0)
    except Exception:
        h3 = False

    # ¬Q: P is not equal to M
    try:
        neg_q = False
        if R in ("ZZ", "Z", S.Integers, ZZ):
            if isinstance(M, (int, sympy.Integer)) and isinstance(P, (int, sympy.Integer)):
                neg_q = (abs(P) != abs(M))
            elif isinstance(M, (list, tuple, set)) and len(M) == 1 and isinstance(P, (list, tuple, set)) and len(P) == 1:
                gen_M = list(M)[0]
                gen_P = list(P)[0]
                if isinstance(gen_M, (int, sympy.Integer)) and isinstance(gen_P, (int, sympy.Integer)):
                    neg_q = (abs(gen_P) != abs(gen_M))
                else:
                    neg_q = (P != M)
            else:
                neg_q = (P != M)
        else:
            neg_q = (P != M)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]