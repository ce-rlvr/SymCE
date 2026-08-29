import sympy
from sympy import Set, S, ProductSet, sympify, Tuple, Matrix, Interval
import math
import itertools
import functools

# Top-level setup: named object bindings
R = S.Reals
R2 = ProductSet(S.Reals, S.Reals)
R3 = ProductSet(S.Reals, S.Reals, S.Reals)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        U = witness.get('U')
        f = witness.get('f')
        a = witness.get('a')
        L_1 = witness.get('L_1')
        L_2 = witness.get('L_2')
    else:
        try:
            U, f, a, L_1, L_2 = witness
        except Exception:
            return [False, False, False, False]

    # H_1: U is an open subset of R^n
    try:
        if U == S.Reals:
            h1 = True
        elif getattr(U, 'is_open', False) == True:
            h1 = True
        elif isinstance(U, ProductSet) and all(getattr(s, 'is_open', False) == True or s == S.Reals for s in U.sets):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: f is a function from U to R^m
    try:
        h2 = callable(f) or hasattr(f, 'free_symbols')
    except Exception:
        h2 = False

    # H_3: a is a point in U
    try:
        h3 = bool(U.contains(sympify(a)))
    except Exception:
        h3 = False

    # ¬Q: L_1 != L_2
    try:
        if hasattr(L_1, 'equals') and hasattr(L_2, 'equals'):
            eq = L_1.equals(L_2)
            if eq is None:
                neg_q = bool(L_1 != L_2)
            else:
                neg_q = not eq
        else:
            neg_q = bool(L_1 != L_2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f is a function from U to R^m",
    "H_3: a is a point in U",
    "¬Q: L_1 != L_2"
]

N_HYP = 3
NEG_Q_INDEX = 3