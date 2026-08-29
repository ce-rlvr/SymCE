import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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

def conditions(witness) -> list[bool]:
    try:
        Z = witness.center() if callable(witness.center) else witness.center
        w_order = witness.order() if callable(witness.order) else witness.order
        z_order = Z.order() if callable(Z.order) else Z.order
        idx = int(w_order) // int(z_order)
        
        factors = factorint(idx)
        h1 = False
        if len(factors) == 1:
            p, exp = list(factors.items())[0]
            if exp == 3:
                h1 = True
    except Exception:
        h1 = False

    try:
        solvable = witness.is_solvable() if callable(witness.is_solvable) else witness.is_solvable
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a prime p such that the index of Z(G) in G is p^3",
    "not Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1