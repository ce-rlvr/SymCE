import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    try:
        G = witness['G']
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        x = witness['x']
        h2 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h2 = False
        
    try:
        H = witness['H']
        if isinstance(H, PermutationGroup):
            # If x is beyond H's degree, all elements of H fix x
            if x >= H.degree:
                stab_H_gens = H.generators
            else:
                stab_H_gens = H.stabilizer(x).generators
            
            # Stab_H(x) == H \cap Stab_G(x) iff Stab_H(x) is a subset of G.
            # This is true iff all generators of Stab_H(x) are in G.
            is_subset = all((g in G) for g in stab_H_gens)
            neg_Q = not is_subset
        else:
            # Fallback if H is provided as an iterable of permutations
            stab_H = [h for h in H if h(x) == x]
            is_subset = all((h in G) for h in stab_H)
            neg_Q = not is_subset
    except Exception:
        neg_Q = False
        
    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X",
    "¬Q: Stab_H(x) != H \\cap Stab_G(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2