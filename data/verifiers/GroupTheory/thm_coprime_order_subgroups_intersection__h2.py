import math
from sympy.combinatorics import PermutationGroup, Permutation
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
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: K is a finite subgroup of G
    try:
        if not isinstance(K, PermutationGroup):
            h2 = False
        else:
            elements_K = set(K.generate())
            elements_G = set(G.generate())
            h2 = elements_K.issubset(elements_G)
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of |H| and |K| is 1
    try:
        if isinstance(H, PermutationGroup):
            size_H = H.order()
        else:
            size_H = len(H)
            
        if isinstance(K, PermutationGroup):
            size_K = K.order()
        else:
            size_K = len(K)
            
        h3 = math.gcd(int(size_H), int(size_K)) == 1
    except Exception:
        h3 = False

    # neg_Q: The intersection H \cap K is NOT the trivial subgroup {e}
    try:
        if isinstance(H, PermutationGroup):
            elements_H = set(H.generate())
        else:
            elements_H = set(H)
            
        if isinstance(K, PermutationGroup):
            elements_K = set(K.generate())
        else:
            elements_K = set(K)
            
        intersection = elements_H.intersection(elements_K)
        
        identity = G.identity
        is_trivial = (len(intersection) == 1) and (identity in intersection)
        neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a finite subgroup of G",
    "H_3: The greatest common divisor of |H| and |K| is 1",
    "¬Q: The intersection H \\cap K is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3