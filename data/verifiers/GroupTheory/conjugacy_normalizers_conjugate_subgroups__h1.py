import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def are_conjugate(G, H, K):
    """Check if subgroups H and K are conjugate in G."""
    if not hasattr(H, 'order') or not hasattr(K, 'order'):
        return False
    if H.order() != K.order():
        return False
    for g in G.elements:
        # Check if g * H * g^-1 is a subset of K
        # Since |H| == |K|, subset implies equality
        if all(K.contains(g * h * g**-1) for h in H.generators):
            return True
    return False

def normalizer(G, H):
    """Compute the normalizer of H in G."""
    norm_elements = []
    for g in G.elements:
        if all(H.contains(g * h * g**-1) for h in H.generators):
            norm_elements.append(g)
    return PermutationGroup(norm_elements)

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (G, H, K)
    """
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    # H_1: Let H and K be subgroups of G
    try:
        h1 = H.is_subgroup(G) and K.is_subgroup(G)
    except Exception:
        h1 = False
        
    # H_2: H and K are conjugate in G
    try:
        h2 = are_conjugate(G, H, K)
    except Exception:
        h2 = False
        
    # ¬Q: The normalizer N_G(H) is NOT conjugate to the normalizer N_G(K) in G
    try:
        N_H = normalizer(G, H)
        N_K = normalizer(G, K)
        neg_q = not are_conjugate(G, N_H, N_K)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H and K are subgroups of G",
    "H_2: H and K are conjugate in G",
    "¬Q: The normalizer N_G(H) is not conjugate to the normalizer N_G(K) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2