import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
    """
    Check the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - G is a solvable group
      - H is a subgroup of G
    Conclusion:
      - H is a solvable group
      
    The witness is expected to be a tuple (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False

    # ¬Q: H is NOT a solvable group
    try:
        neg_q = not bool(H.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2