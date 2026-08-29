import sympy
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

def conditions(witness):
    try:
        G, P, x, y = witness
        h1 = bool(isinstance(G, PermutationGroup) and 
                  isinstance(P, PermutationGroup) and 
                  all(p in G for p in P.generators) and 
                  (x in G) and (y in G))
    except Exception:
        h1 = False

    try:
        G, P, x, y = witness
        h2 = bool((x in P) and (y in P) and 
                  all(x * p == p * x for p in P.generators) and 
                  all(y * p == p * y for p in P.generators))
    except Exception:
        h2 = False

    try:
        G, P, x, y = witness
        h3 = bool(any(g * x * ~g == y for g in G.elements))
    except Exception:
        h3 = False

    try:
        G, P, x, y = witness
        NGP_elements = [g for g in G.elements if all(g * p * ~g in P for p in P.generators)]
        conjugate_in_NGP = bool(any(g * x * ~g == y for g in NGP_elements))
        neg_q = not conjugate_in_NGP
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x and y are elements in the center of P",
    "H_3: x and y are conjugate in G",
    "¬Q: x and y are not conjugate in the normalizer N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3