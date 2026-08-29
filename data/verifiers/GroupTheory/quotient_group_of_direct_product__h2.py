import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness) -> list[bool]:
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]

    # H_1: G_1 and G_2 are groups
    try:
        h1 = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N_2 is a normal subgroup of G_2
    try:
        h2 = bool(isinstance(N2, PermutationGroup) and N2.is_subgroup(G2) and N2.is_normal(G2))
    except Exception:
        h2 = False

    # neg_Q: N_1 x N_2 is NOT a normal subgroup of G_1 x G_2, OR the quotient groups are not isomorphic
    try:
        if not isinstance(N1, PermutationGroup) or not isinstance(N2, PermutationGroup):
            neg_q = True
        else:
            n1_normal = N1.is_subgroup(G1) and N1.is_normal(G1)
            n2_normal = N2.is_subgroup(G2) and N2.is_normal(G2)
            # The conclusion holds if and only if both N1 and N2 are normal subgroups 
            # of G1 and G2 respectively. If either fails, the conclusion fails.
            neg_q = not (n1_normal and n2_normal)
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are groups",
    "H_2: N_2 is a normal subgroup of G_2",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient groups are not isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2