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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The null space of A is always a subspace of the null space of A^T A.
            # Therefore, they are equal if and only if their dimensions are equal.
            ns_A_dim = len(witness.nullspace())
            ns_ATA_dim = len((witness.T * witness).nullspace())
            neg_q = bool(ns_A_dim != ns_ATA_dim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m × n matrix",
    "¬Q: The null space of A^T A is not equal to the null space of A"
]

N_HYP = 1
NEG_Q_INDEX = 1