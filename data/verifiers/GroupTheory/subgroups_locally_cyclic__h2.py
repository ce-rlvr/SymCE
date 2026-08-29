import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_cyclic(group):
    """Check if a finite group is cyclic (which is equivalent to locally cyclic for finite groups)."""
    try:
        if hasattr(group, 'is_cyclic'):
            res = group.is_cyclic
            if res is not None:
                return bool(res)
        
        n = group.order() if callable(group.order) else group.order
        if n == 1:
            return True
        for g in group.elements:
            g_order = g.order() if callable(g.order) else g.order
            if g_order == n:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        # The witness must provide both groups G and H
        if len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a locally cyclic group
    try:
        h1_ok = is_cyclic(G)
    except Exception:
        h1_ok = False
        
    # ¬Q: H is NOT a locally cyclic group
    try:
        neg_q_ok = not is_cyclic(H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a locally cyclic group",
    "¬Q: H is not a locally cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1