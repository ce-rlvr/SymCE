import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def conditions(witness) -> list[bool]:
    # Parse witness: can be a tuple (G, p, n) or just G
    G, p, n = None, None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, n = witness
        else:
            G = witness
            p = G.order()
            n = 1
    except Exception:
        pass

    # H_1: n is a positive integer
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False

    # H_2: G is a finite group of order p^n
    try:
        order = G.order()
        h2 = (order == p**n) and (order > 0) and (order < float('inf'))
    except Exception:
        h2 = False

    # ¬Q: The center of G, Z(G), has order <= 1 (i.e. not strictly greater than 1)
    try:
        if hasattr(G, 'center'):
            c_order = G.center().order()
        else:
            # Fallback for groups without a .center() method
            elements = list(G.generate())
            c_order = sum(1 for g in elements if all(g * h == h * g for h in elements))
        neg_q = (c_order <= 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is a finite group of order p^n",
    "¬Q: The center of G, Z(G), has order <= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2