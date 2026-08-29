import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, M, N = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'order')
    except Exception:
        h1 = False

    # H2: M is a normal subgroup of G
    try:
        h2 = M.is_subgroup(G) and M.is_normal(G)
    except Exception:
        h2 = False

    # H3: G = MN
    try:
        M_elems = list(M.elements) if hasattr(M, 'elements') else list(M)
        N_elems = list(N.elements) if hasattr(N, 'elements') else list(N)
        MN_set = set(m * n for m in M_elems for n in N_elems)
        g_order = G.order() if callable(getattr(G, 'order', None)) else G.order
        h3 = len(MN_set) == g_order
    except Exception:
        h3 = False

    # neg_Q: G/(M \cap N) \cong (G/M) \times (G/N) fails
    try:
        # For the conclusion to hold, G/N must be a valid quotient group, 
        # which requires N to be a normal subgroup of G.
        # If N is normal (and M is normal per H2, and G=MN per H3), 
        # the isomorphism holds by the true Chinese Remainder Theorem for groups.
        # Therefore, the conclusion fails if and only if N is not normal in G.
        if not hasattr(N, 'is_subgroup') or not N.is_subgroup(G):
            neg_q = True
        else:
            neg_q = not N.is_normal(G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: G = MN",
    "¬Q: G/(M \\cap N) is not isomorphic to (G/M) \\times (G/N)"
]

N_HYP = 3
NEG_Q_INDEX = 3