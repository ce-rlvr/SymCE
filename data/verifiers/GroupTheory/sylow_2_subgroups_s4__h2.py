import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)  # Dihedral group of order 8
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is the symmetric group S_4 of degree 4
    # The witness can be either a subgroup P, or a tuple (G, P)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, P = witness
            h1 = G.is_isomorphic(S4) and all(g in G for g in P.generators)
        else:
            P = witness
            h1 = all(g in S4 for g in P.generators)
    except Exception:
        h1 = False

    # ¬Q: P is not isomorphic to the dihedral group D_8 of order 8
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, P = witness
        else:
            P = witness
        
        if P.order() != 8:
            neg_q = True
        else:
            neg_q = not P.is_isomorphic(D4)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_4 of degree 4",
    "¬Q: P is not isomorphic to the dihedral group D_8 of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1