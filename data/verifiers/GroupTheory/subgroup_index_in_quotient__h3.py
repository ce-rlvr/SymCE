import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: N \subseteq H
    try:
        G_elements = set(G.elements) if hasattr(G, 'elements') else set(G.generate())
        N_elements = set(N.elements) if hasattr(N, 'elements') else set(N.generate())
        
        if isinstance(H, PermutationGroup):
            H_elements = set(H.elements) if hasattr(H, 'elements') else set(H.generate())
        else:
            H_elements = set(H)
            
        h3 = N_elements.issubset(H_elements) and H_elements.issubset(G_elements)
    except Exception:
        h3 = False

    # not Q: The index [G:H] is not equal to [G/N : H/N]
    try:
        G_mod_N = set(frozenset(g * n for n in N_elements) for g in G_elements)
        H_mod_N = set(frozenset(h * n for n in N_elements) for h in H_elements)
        
        val_G_N = len(G_mod_N)
        val_H_N = len(H_mod_N)
        
        # Definition A: index is defined as the ratio of sizes |A| / |B|
        defA_fails = (len(G_elements) * val_H_N != val_G_N * len(H_elements))
        
        # Definition B: index is defined as the number of left cosets
        left_cosets_H = set(frozenset(g * h for h in H_elements) for g in G_elements)
        
        left_cosets_H_mod_N = set()
        for g in G_elements:
            coset_g_H_mod_N = frozenset(
                frozenset(g * h * n for n in N_elements) for h in H_elements
            )
            left_cosets_H_mod_N.add(coset_g_H_mod_N)
            
        val_G_N_H_N_cosets = len(left_cosets_H_mod_N)
        
        defB_fails = (len(left_cosets_H) != val_G_N_H_N_cosets)
        
        neg_q = defA_fails or defB_fails
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a subset of H",
    "not Q: The index G:H is not equal to G/N : H/N"
]

N_HYP = 3
NEG_Q_INDEX = 3