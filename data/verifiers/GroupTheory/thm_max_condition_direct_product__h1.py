import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def satisfies_max_condition(grp):
    """
    Checks if a group satisfies the maximum condition on subgroups (i.e., is Noetherian).
    Finite groups and finitely generated abelian groups (like Z) satisfy it.
    """
    if hasattr(grp, "is_PermutationGroup") and grp.is_PermutationGroup:
        return True
    if type(grp).__name__ == 'FreeGroup':
        return len(grp.generators) <= 1
    if type(grp).__name__ == 'FpGroup':
        try:
            ord_g = grp.order()
            if ord_g != float('inf'):
                return True
        except Exception:
            pass
    if isinstance(grp, str):
        grp_upper = grp.upper()
        if grp_upper in ["Z", "Z_N", "FINITE", "TRIVIAL", "S3", "S4", "A4", "D4", "C4", "V4", "Z2", "Z3", "Z4", "Z6"]:
            return True
    return False

def violates_max_condition(grp):
    """
    Checks if a group definitively violates the maximum condition on subgroups.
    Free groups of rank >= 2 and groups like Q, R, C, Q/Z violate it.
    """
    if type(grp).__name__ == 'FreeGroup':
        return len(grp.generators) >= 2
    if isinstance(grp, str):
        grp_upper = grp.upper()
        if grp_upper in ["Q", "R", "C", "F2", "F_2", "FREEGROUP(2)", "F_N", "Q/Z", "Z(P^INF)", "Z[1/P]", "PRUFER"]:
            return True
    return False

def conditions(witness) -> list[bool]:
    # Extract G and H from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: H satisfies the maximum condition on subgroups
    try:
        h1_ok = bool(satisfies_max_condition(H))
    except Exception:
        h1_ok = False

    # ¬Q: G x H does not satisfy the maximum condition on subgroups
    # A direct product G x H satisfies the maximum condition iff BOTH G and H do.
    # Therefore, G x H violates it iff G violates it or H violates it.
    try:
        neg_q = bool(violates_max_condition(G) or violates_max_condition(H))
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H satisfies the maximum condition on subgroups",
    "¬Q: G x H does not satisfy the maximum condition on subgroups"
]

N_HYP = 1
NEG_Q_INDEX = 1