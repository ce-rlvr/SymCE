import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G, n = None, None
    except Exception:
        G, n = None, None

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) >= 2
    except Exception:
        h1 = False

    try:
        if G is None or n is None:
            neg_q = False
        else:
            D = G.derived_subgroup()
            order_D = D.order()
            if order_D != n:
                is_iso = False
            else:
                is_iso = any(g.order() == n for g in D.elements)
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: The commutator subgroup G' is not isomorphic to the cyclic group of order n"
]

N_HYP = 1
NEG_Q_INDEX = 1