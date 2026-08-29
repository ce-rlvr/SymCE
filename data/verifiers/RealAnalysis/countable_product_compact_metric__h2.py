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
    # H_1: {(X_n, d_n)} is a sequence of compact metric spaces
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("X_n_compact", False))
        else:
            h1 = bool(getattr(witness, "X_n_compact", False))
    except Exception:
        h1 = False

    # H_2: D is the product metric on X
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("D_product_metric", False))
        else:
            h2 = bool(getattr(witness, "D_product_metric", False))
    except Exception:
        h2 = False

    # ¬Q: The metric space (X, D) is NOT compact
    try:
        if isinstance(witness, dict):
            q = bool(witness.get("X_compact", True))
        else:
            q = bool(getattr(witness, "X_compact", True))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {(X_n, d_n)} is a sequence of compact metric spaces",
    "H_2: D is the product metric on X",
    "¬Q: The metric space (X, D) is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2