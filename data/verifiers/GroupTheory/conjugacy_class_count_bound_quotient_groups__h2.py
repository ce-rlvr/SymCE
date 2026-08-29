import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def k_quotient(G, N):
    """
    Computes the number of conjugacy classes of the quotient group G/N.
    """
    G_elems = list(G.generate())
    N_elems = list(N.generate())
    
    quotient_classes = set()
    visited = set()
    
    for g in G_elems:
        if g in visited:
            continue
        
        class_elements = set()
        # The conjugacy class of gN in G/N is { x g x^-1 N | x in G }
        # We represent this class by the union of its cosets in G.
        for x in G_elems:
            xgx = x * g * ~x
            for n in N_elems:
                class_elements.add(xgx * n)
        
        visited.update(class_elements)
        quotient_classes.add(frozenset(class_elements))
        
    return len(quotient_classes)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: k(G) is the number of conjugacy classes of G
    try:
        if h1:
            k_G = len(G.conjugacy_classes())
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: k(G/N) is the number of conjugacy classes of the quotient group G/N
    try:
        if h1 and isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G):
            k_G_N = k_quotient(G, N)
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: k(G/N) > k(G)
    try:
        if h2 and h3:
            neg_q = k_G_N > k_G
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k(G) is the number of conjugacy classes of G",
    "H_3: k(G/N) is the number of conjugacy classes of the quotient group G/N",
    "¬Q: k(G/N) > k(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3