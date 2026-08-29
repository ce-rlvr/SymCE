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
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a group
    try:
        h2_ok = isinstance(H, PermutationGroup)
    except Exception:
        h2_ok = False

    # ¬Q: The kernel of phi is not a normal subgroup of G
    try:
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        elif isinstance(phi, list):
            elements = list(G.elements)
            phi_func = lambda x: phi[elements.index(x)]
        else:
            phi_func = phi

        G_elements = list(G.elements)
        id_H = H.identity
        ker_phi = set()
        
        for g in G_elements:
            val = phi_func(g)
            if not H.contains(val):
                raise ValueError("phi maps outside H")
            if val == id_H:
                ker_phi.add(g)
                
        is_normal_subgroup = True
        
        # 1. Must contain the identity
        if G.identity not in ker_phi:
            is_normal_subgroup = False
        else:
            # 2. Must be closed under the group operation
            for a in ker_phi:
                for b in ker_phi:
                    if a * b not in ker_phi:
                        is_normal_subgroup = False
                        break
                if not is_normal_subgroup:
                    break
            
            # 3. Must be closed under inverses
            if is_normal_subgroup:
                for a in ker_phi:
                    if a**-1 not in ker_phi:
                        is_normal_subgroup = False
                        break
            
            # 4. Must be normal (g * k * g^-1 in ker_phi for all g in G, k in ker_phi)
            if is_normal_subgroup:
                for g in G_elements:
                    g_inv = g**-1
                    for k in ker_phi:
                        if g * k * g_inv not in ker_phi:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                        
        neg_q_ok = not is_normal_subgroup
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "¬Q: The kernel of phi is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2