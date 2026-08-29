import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def divides(a, b):
    if a == 0:
        return b == 0
    if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
        return b % a == 0
    try:
        q, r = sympy.div(b, a)
        if r == 0:
            return True
    except Exception:
        pass
    try:
        if sympy.rem(b, a) == 0:
            return True
    except Exception:
        pass
    try:
        ratio = sympy.cancel(b / a)
        if isinstance(ratio, (int, sympy.Integer)) or (hasattr(ratio, 'is_Integer') and ratio.is_Integer):
            return True
        if hasattr(ratio, 'is_polynomial') and ratio.is_polynomial():
            return True
    except Exception:
        pass
    return False

def get_lcm(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return math.lcm(a, b)
    return sympy.lcm(a, b)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    The witness can be a dictionary {'a': a, 'b': b, 'c': c, 'R': R} 
    or a tuple (R, a, b, c) or (a, b, c).
    """
    if isinstance(witness, dict):
        a = witness.get('a')
        b = witness.get('b')
        c = witness.get('c')
        R = witness.get('R', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            R, a, b, c = witness
        elif len(witness) == 3:
            a, b, c = witness
            R = None
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain
    try:
        if R is not None:
            h1 = bool(R.is_UFD)
        else:
            # If no ring is explicitly provided, we assume the standard 
            # domain of the elements (like ZZ or QQ[x]) which are UFDs.
            h1 = True
    except Exception:
        h1 = False

    # H_2: a divides c
    try:
        h2 = bool(divides(a, c))
    except Exception:
        h2 = False

    # H_3: b divides c
    try:
        h3 = bool(divides(b, c))
    except Exception:
        h3 = False

    # ¬Q: lcm(a, b) does NOT divide c
    try:
        l = get_lcm(a, b)
        neg_q = not bool(divides(l, c))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a divides c",
    "H_3: b divides c",
    "¬Q: lcm(a, b) does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3