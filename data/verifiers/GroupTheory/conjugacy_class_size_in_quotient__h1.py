import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import oo

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: g is an element of G",
    "¬Q: The size of the conjugacy class of gN in G/N does not divide the size of the conjugacy class of g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, N, g = witness
    except Exception:
        return [False, False, False]
        
    # H_1: N is a normal subgroup of G
    h1 = False
    try:
        if hasattr(N, 'is_subgroup') and hasattr(N, 'is_normal'):
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
        elif hasattr(N, 'is_normal'):
            h1 = bool(N.is_normal(G))
    except Exception:
        pass
        
    # H_2: g is an element of G
    h2 = False
    try:
        if hasattr(G, '__contains__'):
            h2 = bool(g in G)
        elif hasattr(G, 'elements'):
            h2 = bool(g in G.elements)
    except Exception:
        pass
        
    # ¬Q: The size of the conjugacy class of gN in G/N does not divide the size of the conjugacy class of g in G
    neg_q = False
    
    # Try custom methods first (e.g., for infinite group mock objects)
    try:
        if hasattr(G, 'conjugacy_class_size'):
            c_g = G.conjugacy_class_size(g)
            if hasattr(G, 'quotient_conjugacy_class_size'):
                c_gn = G.quotient_conjugacy_class_size(N, g)
            else:
                c_gn = 1
            if c_gn != 0:
                if c_g == oo:
                    neg_q = True
                else:
                    neg_q = (c_g % c_gn != 0)
            return [h1, h2, neg_q]
    except Exception:
        pass
        
    # Fallback to finite group computation
    try:
        # Size of conjugacy class of g in G
        if hasattr(G, 'conjugacy_class'):
            c_g = len(G.conjugacy_class(g))
        else:
            orbit = set()
            for x in G.elements:
                orbit.add(x * g * x**-1)
            c_g = len(orbit)
            
        # Size of conjugacy class of gN in G/N
        cosets = []
        for x in G.elements:
            conj = x * g * x**-1
            found = False
            for c in cosets:
                try:
                    inv_c = c**-1
                except Exception:
                    inv_c = ~c
                if (inv_c * conj) in N:
                    found = True
                    break
            if not found:
                cosets.append(conj)
        c_gn = len(cosets)
        
        if c_gn != 0:
            if c_g == oo:
                neg_q = True
            else:
                neg_q = (c_g % c_gn != 0)
    except Exception:
        pass
        
    return [h1, h2, neg_q]