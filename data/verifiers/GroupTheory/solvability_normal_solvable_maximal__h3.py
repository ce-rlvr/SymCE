import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: M is a maximal subgroup of G
    try:
        h2 = False
        if h1 and M.order() < G.order() and G.order() % M.order() == 0:
            is_sub = all(g in G for g in M.generators)
            if is_sub:
                is_max = True
                for x in G.generate():
                    if x not in M:
                        H = PermutationGroup(*(list(M.generators) + [x]))
                        if H.order() != G.order():
                            is_max = False
                            break
                h2 = is_max
    except Exception:
        h2 = False

    # H_3: M is a solvable group
    try:
        h3 = bool(M.is_solvable)
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a maximal subgroup of G",
    "H_3: M is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3