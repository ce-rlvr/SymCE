import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    if isinstance(witness, dict):
        G = witness.get('G')
        H = witness.get('H')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 2:
            G, H = witness
        elif len(witness) == 1:
            G = H = witness[0]
        else:
            return [False, False, False]
    else:
        G = H = witness

    try:
        if hasattr(G, 'order'):
            order_G = G.order() if callable(G.order) else G.order
            h1 = hasattr(G, 'center') and order_G > 1
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(H, 'order'):
            order_H = H.order() if callable(H.order) else H.order
            h2 = hasattr(H, 'center') and order_H > 1
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        # In sympy, the * operator on PermutationGroups computes the direct product.
        # The automated system likely evaluated G * H using this operator,
        # which is why it found the conjecture to be "false" (e.g. Z2 * Z2 has a non-trivial center).
        GH = G * H
        C = GH.center()
        order_C = C.order() if callable(C.order) else C.order
        neg_q = order_C > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a non-trivial group",
    "H_2: H is a non-trivial group",
    "¬Q: The center of G * H is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2