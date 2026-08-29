import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import sympy.matrices
from sympy import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

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
    h1 = False
    neg_q = False

    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("h1", False))
            neg_q = bool(witness.get("neg_q", False))
        else:
            if hasattr(witness, "h1"):
                h1 = bool(witness.h1)
            if hasattr(witness, "neg_q"):
                neg_q = bool(witness.neg_q)
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: M is a maximal ideal of R", "not Q: The ideal M(x) is a maximal ideal in the polynomial ring R(x)"]
N_HYP = 1
NEG_Q_INDEX = 1