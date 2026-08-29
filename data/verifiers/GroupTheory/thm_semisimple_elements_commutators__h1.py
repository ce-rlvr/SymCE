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
        G, g = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(g, Permutation) and g in G
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            is_commutator = False
            elements = list(G.elements)
            for x in elements:
                for y in elements:
                    if x * y * ~x * ~y == g:
                        is_commutator = True
                        break
                if is_commutator:
                    break
            neg_q = not is_commutator
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "¬Q: g is not a commutator of any two elements in G"
]

N_HYP = 1
NEG_Q_INDEX = 1