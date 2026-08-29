import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def center_order(G):
    try:
        C = G.center()
        if hasattr(C, 'order'):
            return C.order()
        return len(list(C))
    except Exception:
        pass
    
    try:
        c = 0
        gens = G.generators
        for g in G.elements:
            if all(g * h == h * g for h in gens):
                c += 1
        return c
    except Exception:
        return -1

def conditions(witness):
    try:
        h1_ok = bool(witness.order() > 1)
    except Exception:
        h1_ok = False

    try:
        c_order = center_order(witness)
        neg_q_ok = bool(c_order == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "¬Q: The center Z(G) of G is the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1