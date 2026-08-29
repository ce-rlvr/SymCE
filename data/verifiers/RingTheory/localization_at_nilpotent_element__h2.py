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

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        R, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        if hasattr(R, 'is_commutative') and not R.is_commutative:
            h1 = False
        if hasattr(R, 'has_1') and not R.has_1:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = False
        curr = x
        zero = x - x
        if curr == zero:
            h2 = True
        else:
            for _ in range(100):
                curr = curr * x
                if curr == zero:
                    h2 = True
                    break
    except Exception:
        h2 = False

    try:
        neg_q = not h2
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is nilpotent",
    "¬Q: The localization of R at {1, x, x^2, ...} is not the zero ring"
]

N_HYP = 2
NEG_Q_INDEX = 2