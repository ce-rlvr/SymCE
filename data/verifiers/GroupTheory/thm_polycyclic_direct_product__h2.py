import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
        # The witness should provide both groups G and H.
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
            
        if G is None or H is None:
            return [False, False]
            
        # Ensure both objects are groups by checking for the 'is_solvable' property.
        # In the context of finite groups (which SymPy's PermutationGroup represents),
        # a group is polycyclic if and only if it is solvable.
        if not (hasattr(G, 'is_solvable') and hasattr(H, 'is_solvable')):
            return [False, False]

        # H_1: G is a polycyclic group
        try:
            h1 = bool(G.is_solvable)
        except Exception:
            h1 = False
            
        # ¬Q: The direct product G x H is NOT a polycyclic group
        try:
            # The direct product G x H is polycyclic iff both G and H are polycyclic.
            g_poly = bool(G.is_solvable)
            h_poly = bool(H.is_solvable)
            neg_q = not (g_poly and h_poly)
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a polycyclic group",
    "¬Q: The direct product G x H is not a polycyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1