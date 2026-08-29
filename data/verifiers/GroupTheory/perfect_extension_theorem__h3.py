import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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
        return [False, False, False, False]
    
    # H_1: G and N are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = h1 and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: G/N is a perfect group
    # G/N is perfect iff the derived subgroup of G/N is itself.
    # By the correspondence theorem, this is equivalent to G'N = G.
    try:
        if not h1:
            h3 = False
        else:
            D = G.derived_subgroup()
            gens = list(D.generators) + list(N.generators)
            if not gens:
                # Both D and N are trivial, so G'N is trivial
                h3 = (G.order() == 1)
            else:
                DN = PermutationGroup(gens)
                h3 = (DN.order() == G.order())
    except Exception:
        h3 = False

    # ¬Q: G is not a perfect group
    # G is perfect iff its derived subgroup is equal to G.
    try:
        if not h1:
            neg_q = False
        else:
            neg_q = (G.derived_subgroup().order() != G.order())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and N are groups",
    "H_2: N is a normal subgroup of G",
    "H_3: G/N is a perfect group",
    "¬Q: G is not a perfect group"
]

N_HYP = 3
NEG_Q_INDEX = 3