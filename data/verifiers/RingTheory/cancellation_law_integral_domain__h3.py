import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
x, y, z = sympy.symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            a, b, c = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is an integral domain
    try:
        h1 = True
        if len(witness) == 4:
            R = witness[0]
            if hasattr(R, 'is_domain'):
                h1 = bool(R.is_domain)
    except Exception:
        h1 = False

    # H_2: a, b, c are elements of R
    try:
        def is_valid_element(val):
            if isinstance(val, (int, float, complex)):
                return True
            if hasattr(val, 'is_number') and val.is_number:
                return True
            if hasattr(val, 'is_commutative') and val.is_commutative:
                return True
            return False
        
        h2 = is_valid_element(a) and is_valid_element(b) and is_valid_element(c)
    except Exception:
        h2 = False

    # H_3: ab = ac
    try:
        diff = a * b - a * c
        if hasattr(diff, 'simplify'):
            diff = diff.simplify()
        h3 = (diff == 0)
    except Exception:
        h3 = False

    # ¬Q: b != c
    try:
        diff_bc = b - c
        if hasattr(diff_bc, 'simplify'):
            diff_bc = diff_bc.simplify()
        neg_q = (diff_bc != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: a, b, c are elements of R",
    "H_3: ab = ac",
    "¬Q: b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3