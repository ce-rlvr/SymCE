import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        p, q, G = witness
    except Exception:
        return [False, False]

    # H_1: p, q are coprime integers with p > 0
    try:
        h1 = (isinstance(p, int) and isinstance(q, int) and 
              p > 0 and math.gcd(p, q) == 1)
    except Exception:
        h1 = False

    # neg_Q: G is not isomorphic to Z/pZ
    try:
        if not hasattr(G, 'order') or not hasattr(G, 'elements'):
            neg_q = False
        elif G.order() != p:
            neg_q = True
        else:
            is_cyclic = False
            for g in G.elements:
                if g.order() == p:
                    is_cyclic = True
                    break
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p, q are coprime integers with p > 0",
    "¬Q: G is not isomorphic to Z/pZ"
]

N_HYP = 1
NEG_Q_INDEX = 1