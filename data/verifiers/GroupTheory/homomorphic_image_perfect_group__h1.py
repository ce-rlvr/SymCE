import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) >= 2:
            G = witness[0]
            H = witness[1]
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            G = None
            H = None
    except Exception:
        G = None
        H = None

    try:
        h1_ok = False
        if G is not None and hasattr(G, 'derived_subgroup'):
            h1_ok = bool(G.order() == G.derived_subgroup().order())
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        if H is not None and hasattr(H, 'derived_subgroup'):
            neg_q_ok = bool(H.order() != H.derived_subgroup().order())
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "¬Q: H is not a perfect group"
]

N_HYP = 1
NEG_Q_INDEX = 1