import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        G, H, N, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H3: The index of N in G is finite
    try:
        if h1 and h2:
            # For SymPy PermutationGroups, the order is always finite.
            idx_G_N = G.order() // N.order()
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The index of f(N) in H does not divide the index of N in G
    try:
        if hasattr(f, 'image'):
            f_N = f.image(N)
        else:
            f_N_gens = []
            for g in N.generators:
                try:
                    img = f(g)
                except Exception:
                    img = f[g]
                f_N_gens.append(img)
            f_N = PermutationGroup(f_N_gens)
            
        if not f_N.is_subgroup(H):
            neg_q = False
        else:
            idx_H_fN = H.order() // f_N.order()
            idx_G_N = G.order() // N.order()
            neg_q = (idx_G_N % idx_H_fN != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of N in G is finite",
    "¬Q: The index of f(N) in H does not divide the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3