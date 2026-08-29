import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
)

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
        G1, G2, H1, H2 = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(H1, PermutationGroup) and bool(H1.is_subgroup(G1))
    except Exception:
        h2_ok = False

    try:
        def get_index(G, H):
            if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
                raise ValueError("Not a permutation group")
            if not H.is_subgroup(G):
                raise ValueError("Not a subgroup")
            return G.order() // H.order()
        
        idx1 = get_index(G1, H1)
        idx2 = get_index(G2, H2)
        G_prod = G1 * G2
        H_prod = H1 * H2
        idx_prod = get_index(G_prod, H_prod)
        
        conclusion = (idx_prod == idx1 * idx2)
    except Exception:
        conclusion = False
        
    neg_q = not conclusion

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G1 and G2 are finite groups",
    "H_2: H1 is a subgroup of G1",
    "¬Q: The index of H1xH2 in G1xG2 is not equal to the product of indices"
]

N_HYP = 2
NEG_Q_INDEX = 2