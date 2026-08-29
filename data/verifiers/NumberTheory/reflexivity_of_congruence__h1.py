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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            m = witness.get('m')
        else:
            a, m = witness
    except Exception:
        return [False, False]

    # H_1: m is a positive integer
    try:
        if isinstance(m, int):
            h1 = m > 0
        elif hasattr(m, 'is_integer') and m.is_integer:
            h1 = m > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: a \equiv a \pmod m fails
    try:
        diff = a - a
        concl = (diff % m == 0)
    except Exception:
        concl = False

    neg_q = not concl

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "¬Q: a is not congruent to a mod m"
]

N_HYP = 1
NEG_Q_INDEX = 1