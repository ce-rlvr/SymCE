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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_bi_orderable(G):
    """
    Checks if a group is bi-orderable.
    A bi-orderable group must be torsion-free. 
    For finite groups (which SymPy's PermutationGroup represents), 
    the only torsion-free group is the trivial group.
    """
    try:
        return G.order() == 1
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # The witness should be a tuple of two groups: (G, H)
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a bi-orderable group
    try:
        h1_ok = is_bi_orderable(G)
    except Exception:
        h1_ok = False
        
    # ¬Q: The direct product G x H is NOT a bi-orderable group
    try:
        # In SymPy, the multiplication operator on PermutationGroups gives the direct product
        GxH = G * H
        neg_q_ok = not is_bi_orderable(GxH)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a bi-orderable group",
    "¬Q: G x H is not a bi-orderable group"
]

N_HYP = 1
NEG_Q_INDEX = 1