import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        return [False, False, False]
    
    # H1: G and H are groups
    try:
        h1 = hasattr(G, 'elements') and hasattr(H, 'elements') and hasattr(G, 'identity') and hasattr(H, 'identity')
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if hasattr(N, 'elements') and hasattr(G, 'elements') and hasattr(G, 'identity'):
            N_elements = set(N.elements)
            G_elements = set(G.elements)
            if N_elements.issubset(G_elements) and G.identity in N_elements:
                is_subgroup = True
                for a in N_elements:
                    for b in N_elements:
                        if a * b not in N_elements:
                            is_subgroup = False
                            break
                    if a**-1 not in N_elements:
                        is_subgroup = False
                        break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    h2 = True
                    for g in G_elements:
                        for n in N_elements:
                            if g * n * g**-1 not in N_elements:
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False
        
    # neg_Q: f(N) is not a normal subgroup of H
    try:
        f_N = set()
        if isinstance(f, list):
            f_dict = dict(f)
            for n in N.elements:
                f_N.add(f_dict[n])
        else:
            for n in N.elements:
                if isinstance(f, dict):
                    f_N.add(f[n])
                else:
                    f_N.add(f(n))
                
        H_elements = set(H.elements)
        is_normal = True
        
        if not f_N.issubset(H_elements):
            is_normal = False
        elif H.identity not in f_N:
            is_normal = False
        else:
            # Check closure and inverses
            for a in f_N:
                for b in f_N:
                    if a * b not in f_N:
                        is_normal = False
                        break
                if a**-1 not in f_N:
                    is_normal = False
                    break
                if not is_normal:
                    break
            
            # Check normality
            if is_normal:
                for h in H_elements:
                    for s in f_N:
                        if h * s * h**-1 not in f_N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: N is a normal subgroup of G",
    "¬Q: The image f(N) is not a normal subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2