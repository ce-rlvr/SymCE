import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                h2 = bool(H.is_subgroup(G))
            except Exception:
                h2 = all(G.contains(g) for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G' is not a subgroup of H
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            G_prime = G.derived_subgroup()
            try:
                neg_q = not bool(G_prime.is_subgroup(H))
            except Exception:
                neg_q = not all(H.contains(g) for g in G_prime.generators)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The commutator subgroup G' is not a subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2