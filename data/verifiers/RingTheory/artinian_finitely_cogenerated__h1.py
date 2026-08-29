import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    # H_1: M is an Artinian right R-module
    try:
        h1 = False
        if hasattr(witness, 'is_group') and witness.is_group:
            if witness.order() < float('inf'):
                h1 = True
        elif hasattr(witness, 'shape'):
            h1 = True
    except Exception:
        h1 = False

    # Q: M is finitely cogenerated
    try:
        q = False
        if hasattr(witness, 'is_group') and witness.is_group:
            if witness.order() < float('inf'):
                q = True
        elif hasattr(witness, 'shape'):
            q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is an Artinian right R-module",
    "¬Q: M is not finitely cogenerated"
]

N_HYP = 1
NEG_Q_INDEX = 1