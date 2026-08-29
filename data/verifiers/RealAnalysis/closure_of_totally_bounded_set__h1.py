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
            val = witness.get("A_is_totally_bounded", witness.get("is_totally_bounded", False))
        else:
            val = getattr(witness, "A_is_totally_bounded", getattr(witness, "is_totally_bounded", False))
        
        if callable(val):
            val = val()
        h1 = bool(val)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            val = witness.get("closure_A_is_totally_bounded", witness.get("closure_is_totally_bounded", True))
        else:
            val = getattr(witness, "closure_A_is_totally_bounded", getattr(witness, "closure_is_totally_bounded", True))
            
        if callable(val):
            val = val()
        neg_q = not bool(val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a totally bounded subset of X",
    "¬Q: The closure \\overline{A} is not a totally bounded subset of X"
]

N_HYP = 1
NEG_Q_INDEX = 1