import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_free_group(G):
    """
    Checks if G is a free group.
    We support integers (representing the rank of the free group),
    trivial permutation groups, SymPy FreeGroup, and FpGroup with no relators.
    """
    if isinstance(G, int):
        return G >= 0
    if hasattr(G, 'order') and callable(G.order):
        try:
            if G.order() == 1:
                return True
        except Exception:
            pass
    if type(G).__name__ == 'FreeGroup':
        return True
    if type(G).__name__ == 'FpGroup':
        if hasattr(G, 'relators') and len(G.relators) == 0:
            return True
    return False

def direct_product_is_free(G1, G2):
    """
    The direct product of two free groups is free if and only if 
    at least one of the free groups is the trivial group (rank 0).
    """
    def get_rank(G):
        if isinstance(G, int):
            return G
        if hasattr(G, 'order') and callable(G.order):
            try:
                if G.order() == 1:
                    return 0
            except Exception:
                pass
        if type(G).__name__ == 'FreeGroup':
            return len(G.generators)
        if type(G).__name__ == 'FpGroup':
            if hasattr(G, 'relators') and len(G.relators) == 0:
                return len(G.generators)
        return None

    r1 = get_rank(G1)
    r2 = get_rank(G2)
    
    if r1 is not None and r2 is not None:
        return r1 == 0 or r2 == 0
        
    return False

CONDITION_LABELS = [
    "H_1: F1 and F2 are free groups",
    "¬Q: The direct product F1 x F2 is a free group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        F1, F2 = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(is_free_group(F1) and is_free_group(F2))
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(direct_product_is_free(F1, F2))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]