import sympy
from sympy.combinatorics import PermutationGroup
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
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            h2 = True
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        neg_q = False
        if isinstance(H, PermutationGroup):
            is_semi = True
            for N in H.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    is_semi = False
                    break
            neg_q = not is_semi
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "¬Q: H is not a semisimple group"
]

N_HYP = 2
NEG_Q_INDEX = 2