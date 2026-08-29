import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_free_group(G):
    """
    Check if G represents a free group.
    Integers >= 0 represent the rank of a free group.
    """
    if type(G) in (int, sympy.Integer):
        return int(G) >= 0
    if type(G).__name__ == 'FreeGroup':
        return True
    if hasattr(G, 'order'):
        try:
            # The only finite free group is the trivial group
            return G.order() == 1
        except Exception:
            pass
    if hasattr(G, 'is_trivial'):
        try:
            return bool(G.is_trivial())
        except TypeError:
            return bool(G.is_trivial)
    return False

def is_trivial(G):
    """
    Check if G represents the trivial group.
    """
    if type(G) in (int, sympy.Integer):
        return int(G) == 0
    if type(G).__name__ == 'FreeGroup':
        return len(G.generators) == 0
    if hasattr(G, 'order'):
        try:
            return G.order() == 1
        except Exception:
            pass
    if hasattr(G, 'is_trivial'):
        try:
            return bool(G.is_trivial())
        except TypeError:
            return bool(G.is_trivial)
    return False

def is_non_trivial_free_group(G):
    return is_free_group(G) and not is_trivial(G)

def conditions(witness) -> list[bool]:
    """
    Given a witness (F1, F2), check the remaining hypotheses and the negated conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        F1, F2 = witness
    except Exception:
        return [False, False]
    
    # H_1: F_1 is a non-trivial free group
    try:
        h1 = is_non_trivial_free_group(F1)
    except Exception:
        h1 = False
        
    # ¬Q: F_1 x F_2 IS a free group
    # The direct product of two groups is free if and only if both are free 
    # and at least one of them is the trivial group.
    try:
        neg_q = (is_trivial(F1) and is_free_group(F2)) or (is_trivial(F2) and is_free_group(F1))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F_1 is a non-trivial free group",
    "¬Q: F_1 x F_2 is a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1