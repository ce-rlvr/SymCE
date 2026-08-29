import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

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
        G, N = witness
    except Exception:
        return [False, False, False]

    try:
        order = G.order()
        h1_ok = bool((order > 1 and len(factorint(order)) == 1) or (order == 1))
    except Exception:
        h1_ok = False

    try:
        is_sub = all(G.contains(g) for g in N.generators)
        is_norm = True
        if is_sub:
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        is_norm = False
                        break
        h2_ok = bool(is_sub and is_norm)
    except Exception:
        h2_ok = False

    try:
        Z_elems = set(G.center().elements)
        N_elems = set(N.elements)
        intersection = Z_elems.intersection(N_elems)
        neg_q_ok = bool(len(intersection) == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite p-group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The intersection of N and Z(G) is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2