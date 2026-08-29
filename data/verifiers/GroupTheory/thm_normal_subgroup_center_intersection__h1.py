import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        h1 = True
        # Check if N is a subgroup of G
        for g in N.generators:
            if not G.contains(g):
                h1 = False
                break
        # Check normality condition: g * n * g^-1 in N for all g in G, n in N
        if h1:
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if not N.contains(g * n * g_inv):
                        h1 = False
                        break
    except Exception:
        h1 = False
        
    # H2: N is not the trivial group
    try:
        h2 = bool(N.order() > 1)
    except Exception:
        try:
            h2 = len(list(N.elements)) > 1
        except Exception:
            h2 = False
            
    # neg_Q: The intersection of N and Z(G) is the trivial group
    try:
        neg_q = True
        try:
            n_elems = N.elements
        except Exception:
            n_elems = list(N.generate())
            
        for n in n_elems:
            if n == G.identity or n.is_Identity:
                continue
            
            # Check if n is in the center Z(G)
            in_center = True
            for g in G.generators:
                if n * g != g * n:
                    in_center = False
                    break
            
            if in_center:
                # Found a non-trivial element in N intersect Z(G)
                neg_q = False
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is not the trivial group",
    "¬Q: The intersection of N and Z(G) is the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2