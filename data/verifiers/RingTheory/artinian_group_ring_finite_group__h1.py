import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import ZZ, QQ
import math
import itertools
import functools
import z3

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
    # Extract R and G from the witness
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            G = witness.get('G', Z2)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, G = witness
        else:
            R = witness
            G = Z2
    except Exception:
        return [False, False]

    # H_1: G is a finite group
    try:
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            h1 = order > 0 and order < float('inf')
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: group ring is not a right Artinian ring
    # Since G is finite, the group ring is right Artinian if and only if R is right Artinian.
    try:
        is_art = None
        if R == ZZ:
            is_art = False
        elif hasattr(R, 'is_Field') and R.is_Field:
            is_art = True
        elif type(R).__name__ in ('PolyRing', 'PolynomialRing'):
            is_art = False
        elif type(R).__name__ == 'FractionField':
            is_art = True
            
        if is_art is None:
            neg_q = False
        else:
            neg_q = not is_art
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: G is a finite group", "¬Q: group ring is not right Artinian"]

N_HYP = 1
NEG_Q_INDEX = 1