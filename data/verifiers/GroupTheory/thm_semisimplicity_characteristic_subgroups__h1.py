import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
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

def is_semisimple(G):
    """
    In finite group theory, a semisimple group (often called the layer E(G)) 
    is a central product of quasisimple groups.
    This is equivalent to the group being perfect and its solvable radical 
    being equal to its center.
    """
    try:
        if G.order() == 1:
            return True
        # A semisimple group must be perfect
        if G.derived_subgroup().order() != G.order():
            return False
        
        Z = G.center()
        # The solvable radical must be contained in the center
        for N in G.normal_subgroups():
            if N.is_solvable:
                if not N.is_subgroup(Z):
                    return False
        return True
    except Exception:
        return False

def is_characteristic(G, H):
    """
    Checks if H is a characteristic subgroup of G.
    Since computing the full automorphism group is expensive, we use robust heuristics
    that perfectly identify standard characteristic subgroups (like the center, 
    derived subgroup, or any normal subgroup of unique order).
    """
    try:
        if not H.is_subgroup(G):
            return False
        if not H.is_normal(G):
            return False
        
        # If H is the unique normal subgroup of its order, it must be characteristic
        order_H = H.order()
        count = sum(1 for N in G.normal_subgroups() if N.order() == order_H)
        if count == 1:
            return True
            
        # Fallback: check if H is the center
        Z = G.center()
        if H.is_subgroup(Z) and Z.is_subgroup(H):
            return True
            
        # Fallback: check if H is the derived subgroup
        D = G.derived_subgroup()
        if H.is_subgroup(D) and D.is_subgroup(H):
            return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: G is a semisimple group
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    # H_2: H is a characteristic subgroup of G
    try:
        h2 = is_characteristic(G, H)
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT a semisimple group
    try:
        neg_q = not is_semisimple(H)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: H is a characteristic subgroup of G",
    "¬Q: H is not a semisimple group"
]

N_HYP = 2
NEG_Q_INDEX = 2