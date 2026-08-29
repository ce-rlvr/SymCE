import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
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
            F = witness.get('F', sympy.QQ)
            G = witness.get('G', witness)
        elif isinstance(witness, tuple) and len(witness) == 2:
            F, G = witness
        else:
            F = getattr(witness, 'F', sympy.QQ)
            G = getattr(witness, 'G', witness)
    except Exception:
        F, G = None, None

    try:
        if F is not None:
            h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        if G is not None:
            neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1