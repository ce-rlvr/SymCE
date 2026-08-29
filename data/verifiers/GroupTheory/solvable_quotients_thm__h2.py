import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        return [False, False, False]

    # H_1: G is a group and N is a subgroup of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            # Check if N is a subgroup of G by verifying all generators of N are in G
            h1 = h1 and all(g in G for g in N.generators)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if h1:
            if hasattr(N, 'is_normal'):
                h2 = N.is_normal(G)
            else:
                # Fallback: check if g * n * g^-1 is in N for all generators
                h2 = all((g * n * ~g) in N for n in N.generators for g in G.generators)
    except Exception:
        h2 = False

    # ¬Q: G/N is NOT solvable
    try:
        neg_q = False
        if h1:
            # G/N is solvable iff the derived series of G eventually falls into N.
            # The derived series stabilizes at G.derived_series()[-1].
            # So G/N is solvable iff G.derived_series()[-1] is a subgroup of N.
            G_inf = G.derived_series()[-1]
            is_solvable = all(g in N for g in G_inf.generators)
            neg_q = not is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "H_2: N is a normal subgroup of G",
    "¬Q: G/N is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2