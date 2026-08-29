import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = False
        if N.is_subgroup(G):
            h1 = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        D = N.derived_subgroup()
        neg_q = (D.order() != N.order())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The derived subgroup of N is not equal to N"
]

N_HYP = 1
NEG_Q_INDEX = 1