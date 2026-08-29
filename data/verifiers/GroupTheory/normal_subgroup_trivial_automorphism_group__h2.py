import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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

    # H_1: G is a group and N is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            if hasattr(N, 'is_subgroup'):
                h1 = bool(N.is_subgroup(G))
            else:
                for gen in N.generators:
                    if gen not in G:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: The automorphism group Aut(N) is the trivial group
    # A group has a trivial automorphism group if and only if its order is 1 or 2.
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            h2 = bool(N.order() <= 2)
    except Exception:
        h2 = False

    # ¬Q: N is not contained in the center of G
    # This means there exists some n in N and g in G such that n * g != g * n.
    # It is sufficient to check the generators of N and G.
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            for n in N.generators:
                for g in G.generators:
                    if n * g != g * n:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: The automorphism group Aut(N) is the trivial group",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 2
NEG_Q_INDEX = 2