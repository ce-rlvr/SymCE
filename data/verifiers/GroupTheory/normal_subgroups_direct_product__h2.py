import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings for witness expressions
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def is_normal_subgroup(H, G):
    """Helper to safely check if H is a normal subgroup of G."""
    try:
        if not hasattr(H, 'is_subgroup') or not hasattr(H, 'is_normal'):
            return False
        if not H.is_subgroup(G):
            return False
        return H.is_normal(G)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G1 = witness['G1']
            G2 = witness['G2']
            N1 = witness['N1']
            N2 = witness['N2']
        else:
            G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G1 and G2 are groups
    try:
        h1_ok = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: N2 is a normal subgroup of G2
    try:
        h2_ok = is_normal_subgroup(N2, G2)
    except Exception:
        h2_ok = False
        
    # ¬Q: N1 x N2 is NOT a normal subgroup of G1 x G2
    # N1 x N2 is a normal subgroup of G1 x G2 iff N1 is normal in G1 and N2 is normal in G2.
    try:
        q = is_normal_subgroup(N1, G1) and is_normal_subgroup(N2, G2)
        neg_q_ok = not q
    except Exception:
        # If evaluation fails (e.g. N1 is not a valid group), it cannot form a normal subgroup.
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G1 and G2 are groups",
    "H_2: N2 is a normal subgroup of G2",
    "¬Q: N1 x N2 is not a normal subgroup of G1 x G2"
]

N_HYP = 2
NEG_Q_INDEX = 2