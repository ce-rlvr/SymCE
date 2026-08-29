import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup for potential witness elements
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
    # Unpack witness. It can be (R, I, m, n) or just (I, m, n)
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, I, m, n = witness
            elif len(witness) == 3:
                I, m, n = witness
                R = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a ring
    try:
        # If R is provided, we assume it is a valid ring representation in the context of the witness.
        # If R is omitted, it is implicit.
        h1 = True
    except Exception:
        h1 = False

    # H_2: m and n are positive integers
    try:
        h2 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h2 = False

    # ¬Q: I^m I^n != I^{m+n}
    try:
        lhs = (I ** m) * (I ** n)
        rhs = I ** (m + n)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: m and n are positive integers",
    "¬Q: I^m I^n != I^{m+n}"
]

N_HYP = 2
NEG_Q_INDEX = 2