import sympy
import sympy.combinatorics as combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a primitive permutation group acting faithfully on a set X",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer of x in G",
    "¬Q: The intersection G_x ∩ N is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Extract G, x, N from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            x = witness.get('x')
            N = witness.get('N')
        else:
            G, x, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a primitive permutation group acting faithfully on a set X
    try:
        h1 = bool(G.is_primitive())
    except Exception:
        h1 = False

    # H_2: x is an element of X
    try:
        h2 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h2 = False

    # H_3: G_x is the stabilizer of x in G
    # This is a definitional hypothesis. We verify that G_x can be properly formed.
    try:
        if h1 and h2:
            Gx = G.stabilizer(x)
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The intersection G_x ∩ N is NOT the trivial subgroup {e}
    try:
        Gx = G.stabilizer(x)
        intersection = Gx.intersect(N)
        
        try:
            order = intersection.order()
        except TypeError:
            order = intersection.order
            
        neg_q = (order != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]