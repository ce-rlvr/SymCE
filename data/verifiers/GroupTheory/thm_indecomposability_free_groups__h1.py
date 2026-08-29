import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup,
    PermutationGroup, Permutation
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product(A, B):
    """Helper to compute the direct product of two permutation groups."""
    degA = A.degree
    degB = B.degree
    gens = []
    for g in A.generators:
        arr = [g(i) for i in range(degA)] + list(range(degA, degA + degB))
        gens.append(Permutation(arr))
    for g in B.generators:
        arr = list(range(degA)) + [g(i) + degA for i in range(degB)]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        F, A, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: A and B are subgroups of F
    try:
        if not (isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and isinstance(F, PermutationGroup)):
            h1 = False
        else:
            h1 = all(F.contains(g) for g in A.generators) and all(F.contains(g) for g in B.generators)
    except Exception:
        h1 = False
        
    # H_2: F is isomorphic to the direct product A \times B
    try:
        if not (isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup) and isinstance(F, PermutationGroup)):
            h2 = False
        else:
            DP = direct_product(A, B)
            h2 = F.is_isomorphic(DP)
    except Exception:
        h2 = False
        
    # ¬Q: A is not the trivial group and B is not the trivial group
    try:
        if not (isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)):
            neg_q = False
        else:
            neg_q = bool(A.order() > 1 and B.order() > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are subgroups of F",
    "H_2: F is isomorphic to the direct product A \\times B",
    "¬Q: A is not the trivial group and B is not the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2