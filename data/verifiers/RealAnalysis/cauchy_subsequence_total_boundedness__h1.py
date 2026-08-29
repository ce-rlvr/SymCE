import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
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
    # H_1: Every sequence (x_n) in X contains a subsequence that is a Cauchy sequence.
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('every_sequence_has_cauchy_subsequence', False))
        elif hasattr(witness, 'every_sequence_has_cauchy_subsequence'):
            val = witness.every_sequence_has_cauchy_subsequence
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # ¬Q: The metric space (X, d) is NOT totally bounded.
    neg_q = False
    try:
        q = True
        if isinstance(witness, dict):
            q = bool(witness.get('is_totally_bounded', True))
        elif hasattr(witness, 'is_totally_bounded'):
            val = witness.is_totally_bounded
            q = bool(val() if callable(val) else val)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every sequence (x_n) in X contains a subsequence that is a Cauchy sequence",
    "¬Q: The metric space (X, d) is not totally bounded"
]

N_HYP = 1
NEG_Q_INDEX = 1