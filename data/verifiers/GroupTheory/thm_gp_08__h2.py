import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if len(witness) == 2:
            if isinstance(witness[0], int):
                n, G = witness
            else:
                G, n = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(n, int) and n >= 3
    except Exception:
        h1 = False

    try:
        D2n = DihedralGroup(n)
        if hasattr(G, 'is_isomorphic'):
            if G.order() != D2n.order():
                neg_q = True
            else:
                neg_q = not G.is_isomorphic(D2n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "¬Q: G is not isomorphic to the dihedral group D_{2n}"
]

N_HYP = 1
NEG_Q_INDEX = 1