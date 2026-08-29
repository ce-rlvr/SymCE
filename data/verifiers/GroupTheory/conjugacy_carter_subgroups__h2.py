import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, C1, C2 = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False

    try:
        h2 = bool(C1.is_subgroup(G))
    except Exception:
        h2 = False

    try:
        h3 = bool(C2.is_subgroup(G))
    except Exception:
        h3 = False

    try:
        if C1.order() != C2.order():
            neg_q = True
        else:
            gens1 = C1.generators
            is_conj = False
            for g in G.generate_elements():
                if all((g * x * ~g) in C2 for x in gens1):
                    is_conj = True
                    break
            neg_q = not is_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite solvable group",
    "H_2: C1 is a subgroup of G",
    "H_3: C2 is a subgroup of G",
    "¬Q: C1 and C2 are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3