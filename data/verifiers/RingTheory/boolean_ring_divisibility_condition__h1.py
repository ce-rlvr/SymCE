import math
import itertools
import functools
import sympy
from sympy import symbols, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                a, b = witness
            elif len(witness) == 3:
                _, a, b = witness
            else:
                a, b = None, None
        else:
            a, b = None, None
    except Exception:
        a, b = None, None

    # H_1: a and b are elements of R
    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            h1 = True
        elif isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: (a divides b) is not equivalent to (ab = b)
    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            if a == 0:
                divides = (b == 0)
            else:
                divides = (b % a == 0)
            ab_eq_b = (a * b == b)
            neg_q = bool(divides != ab_eq_b)
        elif h1:
            q, r = sympy.div(b, a)
            divides = (r == 0)
            ab_eq_b = (sympy.simplify(a * b - b) == 0)
            neg_q = bool(divides != ab_eq_b)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of a ring",
    "¬Q: (a divides b) is not equivalent to (ab = b)"
]

N_HYP = 1
NEG_Q_INDEX = 1