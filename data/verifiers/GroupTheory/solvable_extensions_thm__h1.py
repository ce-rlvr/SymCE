import sympy
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and G.is_normal(N))
    except Exception:
        h1 = False

    # H_2: N is a solvable group
    try:
        h2 = bool(N.is_solvable)
    except Exception:
        h2 = False

    # H_3: The quotient group G/N is solvable
    # G/N is solvable iff the derived series of G eventually lands inside N
    try:
        h3 = False
        if h1:
            for H in G.derived_series():
                if H.is_subgroup(N):
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a solvable group",
    "H_3: The quotient group G/N is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3