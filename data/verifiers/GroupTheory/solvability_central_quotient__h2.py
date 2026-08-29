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
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The quotient group G/Z(G) is solvable
    # G/Z(G) is solvable iff the derived series of G eventually lands in Z(G)
    try:
        if h1:
            Z = witness.center
            if callable(Z):
                Z = Z()
            
            ds = witness.derived_series
            if callable(ds):
                ds = ds()
                
            # Check if the last subgroup in the derived series is a subgroup of the center
            h2 = all(g in Z for g in ds[-1].generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    try:
        if h1:
            solv = witness.is_solvable
            if callable(solv):
                solv = solv()
            neg_q = not solv
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2