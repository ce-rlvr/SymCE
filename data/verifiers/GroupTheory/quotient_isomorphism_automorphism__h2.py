import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        G, N, alpha = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
        if h1:
            G_elems = list(G.elements)
            for gen in N.generators:
                if gen not in G_elems:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: alpha is an automorphism of G
    try:
        h2 = True
        G_elems = list(G.elements)
        
        if callable(alpha):
            alpha_dict = {g: alpha(g) for g in G_elems}
        elif isinstance(alpha, dict):
            alpha_dict = alpha
        else:
            h2 = False
            alpha_dict = {}
            
        if h2:
            if len(set(alpha_dict.values())) != len(G_elems):
                h2 = False
            else:
                for g in G_elems:
                    if g not in alpha_dict or alpha_dict[g] not in G_elems:
                        h2 = False
                        break
                    for h in G_elems:
                        if alpha_dict[g * h] != alpha_dict[g] * alpha_dict[h]:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # neg_Q: The image \alpha(N) is a normal subgroup of G, and the quotient group G/N is isomorphic to G/\alpha(N)
    try:
        G_elems = list(G.elements)
        if callable(alpha):
            alpha_dict = {g: alpha(g) for g in G_elems}
        else:
            alpha_dict = alpha
            
        N_elems = list(N.elements)
        N_elems_set = set(N_elems)
        
        if not N_elems:
            conclusion = False
        else:
            is_N_subgroup = True
            for x in N_elems:
                for y in N_elems:
                    if x * y not in N_elems_set:
                        is_N_subgroup = False
                        break
                if not is_N_subgroup:
                    break
                    
            is_N_normal = True
            if is_N_subgroup:
                for g in G_elems:
                    g_inv = ~g
                    for n in N_elems:
                        if g * n * g_inv not in N_elems_set:
                            is_N_normal = False
                            break
                    if not is_N_normal:
                        break
            else:
                is_N_normal = False

            alpha_N_elems = [alpha_dict[n] for n in N_elems]
            alpha_N_set = set(alpha_N_elems)
            
            is_alpha_N_subgroup = True
            for x in alpha_N_elems:
                for y in alpha_N_elems:
                    if x * y not in alpha_N_set:
                        is_alpha_N_subgroup = False
                        break
                if not is_alpha_N_subgroup:
                    break
                    
            is_alpha_N_normal = True
            if is_alpha_N_subgroup:
                for g in G_elems:
                    g_inv = ~g
                    for n in alpha_N_elems:
                        if g * n * g_inv not in alpha_N_set:
                            is_alpha_N_normal = False
                            break
                    if not is_alpha_N_normal:
                        break
            else:
                is_alpha_N_normal = False
                    
            conclusion = is_alpha_N_normal and is_N_normal
            
        neg_q = not conclusion
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: alpha is an automorphism of G",
    "¬Q: alpha(N) is not a normal subgroup of G, or G/N is not isomorphic to G/alpha(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2