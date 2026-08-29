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

def conditions(witness):
    G = witness
    Z = None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Z = witness

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        elif Z is not None:
            C = G.center()
            if isinstance(Z, PermutationGroup):
                try:
                    h2 = all(C.contains(g) for g in Z.generators) and all(Z.contains(g) for g in C.generators)
                except AttributeError:
                    h2 = all((g in C) for g in Z.generators) and all((g in Z) for g in C.generators)
            else:
                h2 = False
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        if h1:
            neg_q = not G.is_abelian
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2