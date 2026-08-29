import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: phi is a group homomorphism from G to H",
    "H_3: N is a subset of ker(phi)",
    "¬Q: G/N is not a group (N is not a normal subgroup of G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, H, phi_dict, N_list = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: phi is a group homomorphism from G to H
    try:
        h2 = True
        if not h1:
            h2 = False
        elif not isinstance(phi_dict, dict):
            h2 = False
        else:
            G_elements = list(G.elements)
            H_elements = list(H.elements)
            for g in G_elements:
                if g not in phi_dict:
                    h2 = False
                    break
                if phi_dict[g] not in H_elements:
                    h2 = False
                    break
            if h2:
                for x in G_elements:
                    for y in G_elements:
                        if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: N is a subset of ker(phi)
    try:
        h3 = True
        if not h1:
            h3 = False
        elif not isinstance(N_list, (list, set, tuple)):
            h3 = False
        else:
            G_elements = list(G.elements)
            e_H = H.identity
            for n in N_list:
                if n not in G_elements:
                    h3 = False
                    break
                if n not in phi_dict:
                    h3 = False
                    break
                if phi_dict[n] != e_H:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: The conclusion fails (G/N is not a group, which happens iff N is not a normal subgroup of G)
    try:
        if not h1:
            neg_q = False
        elif not isinstance(N_list, (list, set, tuple)):
            neg_q = False
        else:
            G_elements = list(G.elements)
            is_subgroup = True
            e_G = G.identity
            
            # Check if N is a subgroup
            if e_G not in N_list:
                is_subgroup = False
            else:
                for n1 in N_list:
                    for n2 in N_list:
                        if n1 * n2 not in N_list:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                    if n1**-1 not in N_list:
                        is_subgroup = False
                        break
            
            # Check if N is normal
            is_normal = is_subgroup
            if is_normal:
                for g in G_elements:
                    for n in N_list:
                        if g * n * (g**-1) not in N_list:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]