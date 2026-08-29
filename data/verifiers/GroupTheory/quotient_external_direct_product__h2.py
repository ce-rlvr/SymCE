import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
V4 = PermutationGroup([Permutation(0, 1), Permutation(2, 3)])

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are groups",
    "H_2: N_2 is a normal subgroup of G_2",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient isomorphism fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G_1 and G_2 are groups (and N_1, N_2 are valid subgroups to form the quotients)
    try:
        h1 = (isinstance(G1, PermutationGroup) and 
              isinstance(G2, PermutationGroup) and 
              isinstance(N1, PermutationGroup) and 
              isinstance(N2, PermutationGroup) and 
              bool(N1.is_subgroup(G1)) and 
              bool(N2.is_subgroup(G2)))
    except Exception:
        h1 = False

    # H_2: N_2 is a normal subgroup of G_2
    try:
        h2 = bool(N2.is_subgroup(G2) and G2.is_normal(N2))
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # The conclusion states that N_1 x N_2 is normal in G_1 x G_2 AND the isomorphism holds.
    # Mathematically, N_1 x N_2 is normal in G_1 x G_2 if and only if N_1 is normal in G_1 
    # and N_2 is normal in G_2. If both are normal, the isomorphism is guaranteed by the true theorem.
    # Therefore, the conclusion fails if and only if either N_1 is not normal in G_1 or N_2 is not normal in G_2.
    try:
        is_normal_1 = bool(N1.is_subgroup(G1) and G1.is_normal(N1))
        is_normal_2 = bool(N2.is_subgroup(G2) and G2.is_normal(N2))
        neg_q = not (is_normal_1 and is_normal_2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]