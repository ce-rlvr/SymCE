import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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
        G, p = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        Z = G.center()
        is_cyclic_order_p = False
        if Z.order() == p:
            if p == 1:
                is_cyclic_order_p = True
            else:
                for g in Z.elements:
                    if g.order() == p:
                        is_cyclic_order_p = True
                        break
        neg_q = not is_cyclic_order_p
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "¬Q: The center Z(G) is not a cyclic group of order p"
]

N_HYP = 1
NEG_Q_INDEX = 1