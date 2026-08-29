import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
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
    """
    Given a witness (G1, G2, N1, N2), check the remaining hypotheses and the negated conclusion.
    """
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G1 and G2 are groups
    try:
        h1_ok = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: N1 is a normal subgroup of G1
    try:
        h2_ok = bool(isinstance(N1, PermutationGroup) and N1.is_subgroup(G1) and N1.is_normal(G1))
    except Exception:
        h2_ok = False
        
    # ¬Q: The conclusion FAILS.
    # The conclusion is that the quotient group (G1 × G2) / (N1 × N2) is isomorphic to (G1 / N1) × (G2 / N2).
    # This mathematically holds if and only if N2 is a normal subgroup of G2.
    # If N2 is not a normal subgroup of G2, the quotient (G1 × G2) / (N1 × N2) is not a group,
    # so the isomorphism statement is false.
    try:
        if not isinstance(N2, PermutationGroup):
            neg_q_ok = True
        elif not N2.is_subgroup(G2):
            neg_q_ok = True
        elif not N2.is_normal(G2):
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G1 and G2 are groups",
    "H_2: N1 is a normal subgroup of G1",
    "¬Q: The quotient group (G1 × G2) / (N1 × N2) is not isomorphic to (G1 / N1) × (G2 / N2)"
]

N_HYP = 2
NEG_Q_INDEX = 2