import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup for potential witness expressions
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

def is_group(grp):
    """Check if the object is a SymPy PermutationGroup."""
    return isinstance(grp, PermutationGroup)

def is_torsion_free(grp):
    """
    A group is torsion-free if its only element of finite order is the identity.
    For finite groups (like PermutationGroup), this is true if and only if 
    the group is the trivial group (order 1).
    """
    if not is_group(grp):
        return False
    try:
        return grp.order() == 1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1_ok = is_group(G) and is_group(H)
    except Exception:
        h1_ok = False

    # H_2: H is torsion-free
    try:
        h2_ok = is_torsion_free(H)
    except Exception:
        h2_ok = False

    # ¬Q: The direct product G x H is NOT a torsion-free group.
    # The direct product of two groups is torsion-free if and only if 
    # BOTH groups are torsion-free. Thus, it is NOT torsion-free if 
    # at least one of them is not torsion-free.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            neg_q_ok = not (is_torsion_free(G) and is_torsion_free(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: H is torsion-free",
    "¬Q: G x H is not torsion-free"
]

N_HYP = 2
NEG_Q_INDEX = 2