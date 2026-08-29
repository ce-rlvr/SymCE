import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

def safe_direct_product(G, H):
    n = G.degree
    m = H.degree
    gens = []
    for g in G.generators:
        arr = [g(i) for i in range(n)] + list(range(n, n + m))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = list(range(n)) + [h(i) + n for i in range(m)]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation()])
    return PermutationGroup(gens)

def are_isomorphic(G, H):
    if not hasattr(G, 'order') or not hasattr(H, 'order'):
        return False
    if G.order() != H.order():
        return False
    if getattr(G, 'is_abelian', False) != getattr(H, 'is_abelian', False):
        return False
    if getattr(G, 'is_abelian', False):
        return sorted(G.abelian_invariants()) == sorted(H.abelian_invariants())
    try:
        return G.is_isomorphic(H)
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        A, B, C = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: A is a finite abelian group
    try:
        h1 = getattr(A, 'is_abelian', False) and A.order() < float('inf')
    except Exception:
        h1 = False

    # H2: C is a finite abelian group
    try:
        h2 = getattr(C, 'is_abelian', False) and C.order() < float('inf')
    except Exception:
        h2 = False

    # H3: The direct sum A ⊕ B is isomorphic to A ⊕ C
    try:
        A_oplus_B = safe_direct_product(A, B)
        A_oplus_C = safe_direct_product(A, C)
        h3 = are_isomorphic(A_oplus_B, A_oplus_C)
    except Exception:
        h3 = False

    # neg_Q: The group B is NOT isomorphic to the group C
    try:
        neg_q = not are_isomorphic(B, C)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: C is a finite abelian group",
    "H_3: The direct sum A ⊕ B is isomorphic to A ⊕ C",
    "¬Q: The group B is not isomorphic to the group C"
]

N_HYP = 3
NEG_Q_INDEX = 3