import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_invariants(G):
    """
    Extracts the invariant factors (or order) of an abelian group.
    Returns a list of integers representing the cyclic factors, or None if invalid.
    """
    if isinstance(G, (list, tuple)):
        if all(isinstance(x, int) and x >= 0 for x in G):
            return list(G)
    if hasattr(G, 'is_abelian'):
        if not G.is_abelian:
            return None
        if hasattr(G, 'order'):
            try:
                o = int(G.order())
                return [o]
            except Exception:
                pass
    return None

def is_torsion_abelian(G):
    """
    Checks if G is a torsion abelian group.
    """
    if isinstance(G, (list, tuple)):
        if not all(isinstance(x, int) and x >= 0 for x in G):
            return False
        # In our list representation, 0 means Z (which is not torsion).
        # Any positive integer n means Z/nZ (which is torsion).
        return all(x > 0 for x in G)
    if hasattr(G, 'is_abelian') and hasattr(G, 'order'):
        try:
            if not G.is_abelian:
                return False
            o = int(G.order())
            return o > 0
        except Exception:
            return False
    return False

def neg_q_condition(D, T):
    """
    Checks if the tensor product D \otimes T is NOT the trivial group.
    """
    inv_D = get_invariants(D)
    inv_T = get_invariants(T)
    if inv_D is None or inv_T is None:
        return False
    
    # The tensor product of \oplus Z/d_i and \oplus Z/t_j is \oplus Z/gcd(d_i, t_j).
    # It is trivial iff all gcds are 1.
    for d in inv_D:
        for t in inv_T:
            if math.gcd(d, t) != 1:
                return True
    return False

def conditions(witness):
    """
    Given a witness (D, T), checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        D, T = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_torsion_abelian(T)
    except Exception:
        h1 = False
        
    try:
        neg_q = neg_q_condition(D, T)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a torsion abelian group",
    "¬Q: The tensor product D \\otimes_\\mathbb{Z} T is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1