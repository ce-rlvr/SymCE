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

# Top-level setup: named object bindings
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
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1_ok, neg_Q_ok]
    """
    h1_ok = False
    neg_q_ok = False

    try:
        if isinstance(witness, dict):
            h1_ok = bool(witness.get("is_Artinian", witness.get("is_artinian", False)))
            q_ok = bool(witness.get("is_finite_direct_sum_of_indecomposables", witness.get("is_finite_decomposition", True)))
            neg_q_ok = not q_ok
        else:
            h1_ok = bool(getattr(witness, "is_Artinian", getattr(witness, "is_artinian", False)))
            q_ok = bool(getattr(witness, "is_finite_direct_sum_of_indecomposables", getattr(witness, "is_finite_decomposition", True)))
            neg_q_ok = not q_ok
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is an Artinian right R-module",
    "¬Q: M cannot be expressed as a direct sum of a finite number of indecomposable submodules"
]

N_HYP = 1
NEG_Q_INDEX = 1