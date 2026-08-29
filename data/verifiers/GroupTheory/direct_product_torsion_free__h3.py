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

def is_group(obj):
    if isinstance(obj, PermutationGroup):
        return True
    if hasattr(obj, 'elements') and hasattr(obj, 'order'):
        return True
    return False

def is_torsion_free(grp):
    try:
        if hasattr(grp, 'order'):
            order = grp.order() if callable(grp.order) else grp.order
            if order == 1:
                return True
            if isinstance(grp, PermutationGroup):
                return False
        
        for g in grp.elements:
            o = g.order() if callable(g.order) else g.order
            if o > 1:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = is_group(G) and is_group(H)
    except Exception:
        h1 = False

    try:
        h2 = is_torsion_free(G)
    except Exception:
        h2 = False

    try:
        # G x H is torsion-free iff both G and H are torsion-free.
        # Therefore, G x H is NOT torsion-free iff at least one of them has torsion.
        if is_group(G) and is_group(H):
            neg_q = not (is_torsion_free(G) and is_torsion_free(H))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is torsion-free",
    "¬Q: G x H is not torsion-free"
]

N_HYP = 2
NEG_Q_INDEX = 2