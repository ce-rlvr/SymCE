import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup for potential witness expressions
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

def is_subgroup(sub, super_group):
    """Robust subgroup check that handles permutation degree differences."""
    try:
        if not isinstance(sub, PermutationGroup) or not isinstance(super_group, PermutationGroup):
            return False
        degree = super_group.degree
        for g in sub.generators:
            if g.size < degree:
                g_padded = Permutation(g.array_form + list(range(g.size, degree)))
            elif g.size > degree:
                if any(g(i) != i for i in range(degree, g.size)):
                    return False
                g_padded = Permutation(g.array_form[:degree])
            else:
                g_padded = g
            if not super_group.contains(g_padded):
                return False
        return True
    except Exception:
        return False

def get_index(A, B):
    """
    Computes the number of left cosets of B in A.
    If B is a subgroup of A, this is exactly the index [A:B].
    If B is not a subgroup of A, this computes [A : A \cap B].
    """
    cosets = set()
    B_els = list(B.elements)
    for a in A.elements:
        coset = frozenset(a * b for b in B_els)
        cosets.add(coset)
    return len(cosets)

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: H is a subgroup of G
    try:
        h2 = is_subgroup(H, G)
    except Exception:
        h2 = False
        
    # H3: The index of H in G is finite
    try:
        # For finite permutation groups, the index is always finite
        h3 = h2 and True
    except Exception:
        h3 = False
        
    # H4: The index of K in H is finite
    try:
        # K must be a valid group for the index to be well-defined and finite
        h4 = isinstance(K, PermutationGroup)
    except Exception:
        h4 = False
        
    # neg_Q: The index of K in G is finite and equals the product of the index of H in G and the index of K in H
    try:
        idx_G_H = get_index(G, H)
        idx_H_K = get_index(H, K)
        idx_G_K = get_index(G, K)
        
        # The conclusion fails if the indices do not satisfy the multiplicative property
        neg_q = (idx_G_K != idx_G_H * idx_H_K)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is finite",
    "H_4: The index of K in H is finite",
    "¬Q: The index of K in G is not finite or does not equal the product of the index of H in G and the index of K in H"
]

N_HYP = 4
NEG_Q_INDEX = 4