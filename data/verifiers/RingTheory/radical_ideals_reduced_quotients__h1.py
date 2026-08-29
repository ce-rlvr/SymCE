import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_ideal', False))
        else:
            h1 = bool(getattr(witness, 'is_ideal', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            is_rad = bool(witness.get('is_radical', False))
            has_nilp = bool(witness.get('has_nilpotent', False))
        else:
            is_rad = bool(getattr(witness, 'is_radical', False))
            has_nilp = bool(getattr(witness, 'has_nilpotent', False))
        
        neg_q = (is_rad == has_nilp)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The equivalence (I == radical(I) iff R/I has no non-zero nilpotents) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1