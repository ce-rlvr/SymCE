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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_compact', False) and witness.get('is_metric', False))
        elif isinstance(witness, sympy.Set):
            # For subsets of R^n in SymPy, compact is equivalent to closed and bounded
            h1 = bool(witness.is_closed and witness.is_bounded)
        else:
            h1 = bool(getattr(witness, 'is_compact', False) and getattr(witness, 'is_metric', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('C_X_is_separable', True))
        elif isinstance(witness, sympy.Set):
            # For any compact subset of R^n, C(X) is separable
            neg_q = False
        else:
            neg_q = not bool(getattr(witness, 'C_X_is_separable', True))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a compact metric space",
    "¬Q: The Banach space C(X) is not separable"
]

N_HYP = 1
NEG_Q_INDEX = 1