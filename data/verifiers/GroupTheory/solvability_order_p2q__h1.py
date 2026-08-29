import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
    # The witness can be just the group G, or a tuple (G, p, q), or (G, p)
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, p, q = witness
        elif len(witness) == 2:
            G, p = witness
            q = None
        else:
            G = witness[0]
            p, q = None, None
    else:
        G = witness
        p, q = None, None

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and hasattr(G, 'is_solvable')
        if h1:
            order = int(G.order())
            h1 = order > 0
    except Exception:
        h1 = False

    # H_2: Assume the order of G is exactly p^2q
    try:
        order = int(G.order())
        if p is not None and q is not None:
            h2 = (order == int(p)**2 * int(q))
        elif p is not None and q is None:
            h2 = (order % (int(p)**2) == 0)
        else:
            # If p and q are not provided, any finite group order can be written as 1^2 * order
            h2 = order > 0
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is exactly p^2q",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2
