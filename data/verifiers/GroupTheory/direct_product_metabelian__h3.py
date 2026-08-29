import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a metabelian group
    try:
        # A group is metabelian if its commutator (derived) subgroup is abelian.
        h2 = bool(G.derived_subgroup().is_abelian)
    except Exception:
        h2 = False

    # ¬Q: The direct product G x H is NOT a metabelian group
    try:
        try:
            # Attempt to construct the direct product explicitly
            GxH = G * H
            neg_q = not bool(GxH.derived_subgroup().is_abelian)
        except Exception:
            # Fallback: (G x H)' = G' x H', which is abelian iff both G' and H' are abelian.
            # Assuming H_2 holds (G' is abelian), G x H is metabelian iff H' is abelian.
            neg_q = not bool(H.derived_subgroup().is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a metabelian group",
    "¬Q: G x H is not a metabelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2