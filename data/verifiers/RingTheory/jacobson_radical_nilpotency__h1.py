import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Extract R and J from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, J = witness
        elif isinstance(witness, dict) and 'R' in witness and 'J' in witness:
            R = witness['R']
            J = witness['J']
        elif hasattr(witness, 'R') and hasattr(witness, 'J'):
            R = witness.R
            J = witness.J
        else:
            R = witness
            if hasattr(R, 'jacobson_radical'):
                val = getattr(R, 'jacobson_radical')
            else:
                val = getattr(R, 'radical')
            J = val() if callable(val) else val
    except Exception:
        return [False, False, False]

    # H_1: R is a left Artinian ring
    try:
        if hasattr(R, 'is_left_artinian'):
            val = getattr(R, 'is_left_artinian')
        else:
            val = getattr(R, 'is_artinian')
        h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # H_2: J(R) is the Jacobson radical of R
    try:
        if hasattr(R, 'jacobson_radical'):
            val = getattr(R, 'jacobson_radical')
        else:
            val = getattr(R, 'radical')
        expected_J = val() if callable(val) else val
        h2 = bool(J == expected_J)
    except Exception:
        h2 = False

    # ¬Q: J(R) is not a nilpotent ideal
    try:
        val = getattr(J, 'is_nilpotent')
        neg_q = not bool(val() if callable(val) else val)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a left Artinian ring",
    "H_2: J(R) is the Jacobson radical of R",
    "¬Q: J(R) is not a nilpotent ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2