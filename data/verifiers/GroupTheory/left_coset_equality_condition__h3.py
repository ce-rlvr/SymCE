import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H, b, a = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: b is an element of G
    try:
        h3 = b in G.elements
    except Exception:
        h3 = False

    # neg_Q: aH == bH iff ~a * b in H
    try:
        def compute_coset(x, H_group):
            if isinstance(x, (set, list, tuple, frozenset)):
                return set(elem * h for elem in x for h in H_group.elements)
            elif hasattr(x, 'elements'):
                return set(elem * h for elem in x.elements for h in H_group.elements)
            else:
                return set(x * h for h in H_group.elements)
        
        aH = compute_coset(a, H)
        bH = compute_coset(b, H)
        left_eq = (aH == bH)
    except Exception:
        left_eq = False

    try:
        if isinstance(a, (set, list, tuple, frozenset)) or hasattr(a, 'elements'):
            # If a is a subset/subgroup, a^{-1}b is not a valid element expression in this context
            right_in = False
        else:
            right_in = (~a * b) in H.elements
    except Exception:
        right_in = False

    try:
        neg_q = (left_eq != right_in)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: b is an element of G",
    "¬Q: The left coset aH is equal to the left coset bH if and only if a^{-1}b is an element of H fails"
]

N_HYP = 3
NEG_Q_INDEX = 3