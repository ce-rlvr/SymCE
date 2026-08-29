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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H) where G is a group and H is a subgroup.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a subgroup of G
    try:
        h1_ok = (isinstance(H, PermutationGroup) and 
                 isinstance(G, PermutationGroup) and 
                 all(g in G for g in H.generators))
    except Exception:
        h1_ok = False

    # neg_Q: H is not locally cyclic
    # Note: For finite groups (which SymPy's PermutationGroup represents), 
    # being locally cyclic is equivalent to being cyclic.
    try:
        neg_q_ok = isinstance(H, PermutationGroup) and not bool(H.is_cyclic)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not locally cyclic (not cyclic)"
]

N_HYP = 1
NEG_Q_INDEX = 1