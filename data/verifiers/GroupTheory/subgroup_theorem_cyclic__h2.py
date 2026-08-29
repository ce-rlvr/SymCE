import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_cyclic(group):
    """Helper to check if a permutation group is cyclic."""
    try:
        if hasattr(group, 'is_cyclic') and group.is_cyclic is not None:
            return bool(group.is_cyclic)
    except Exception:
        pass
    try:
        order = group.order()
        for g in group.elements:
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a cyclic group
    try:
        if not isinstance(G, PermutationGroup):
            h1_ok = False
        else:
            h1_ok = is_cyclic(G)
    except Exception:
        h1_ok = False
        
    # ¬Q: H is NOT a cyclic group
    try:
        if not isinstance(H, PermutationGroup):
            neg_q_ok = False
        else:
            neg_q_ok = not is_cyclic(H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1