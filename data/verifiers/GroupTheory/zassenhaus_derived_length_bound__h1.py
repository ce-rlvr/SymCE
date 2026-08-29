import math
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    # The witness can be either a group G, or a tuple (G, c)
    if isinstance(witness, tuple) and len(witness) == 2:
        G, c = witness
    else:
        G = witness
        try:
            c = getattr(G, "nilpotency_class", None)
            if callable(c):
                c = c()
        except Exception:
            c = None

    # H_1: The nilpotency class of G is c
    try:
        actual_c = getattr(G, "nilpotency_class", None)
        if callable(actual_c):
            actual_c = actual_c()
            
        if actual_c is False or actual_c is None:
            h1 = False
        else:
            h1 = bool(actual_c == c)
    except Exception:
        h1 = False

    # neg_Q: The derived length of G is greater than ceil(log2(c+1))
    try:
        d = getattr(G, "derived_length", None)
        if callable(d):
            d = d()
            
        if d is False or d is None or c is None or c is False:
            neg_q = False
        else:
            c_val = int(c)
            if c_val < 0:
                neg_q = False
            else:
                bound = math.ceil(math.log2(c_val + 1))
                neg_q = bool(d > bound)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The nilpotency class of G is c",
    "¬Q: The derived length of G is greater than ceil(log2(c+1))"
]

N_HYP = 1
NEG_Q_INDEX = 1