import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = DihedralGroup(2)
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
        return [False, False]
        
    phi_dict = {}
    try:
        G_elements = list(G.generate())
    except Exception:
        return [False, False]

    # H_1: phi is a group homomorphism from G to H
    h1_ok = False
    try:
        if callable(phi):
            phi_dict = {x: phi(x) for x in G_elements}
        elif isinstance(phi, dict):
            phi_dict = phi
            
        domain_ok = set(phi_dict.keys()) == set(G_elements)
        codomain_ok = all(v in H for v in phi_dict.values())
        
        if domain_ok and codomain_ok:
            hom_ok = True
            for x in G_elements:
                for y in G_elements:
                    if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                        hom_ok = False
                        break
                if not hom_ok:
                    break
            h1_ok = hom_ok
    except Exception:
        h1_ok = False

    # neg_Q: The quotient group G/ker(phi) is NOT isomorphic to the subgroup phi(G) of H
    neg_q_ok = False
    try:
        if not phi_dict:
            return [h1_ok, False]
            
        H_id = H.identity
        K_elements = set(x for x in G_elements if phi_dict.get(x) == H_id)
        
        # Check if K = ker(phi) is a subgroup
        is_subgroup = True
        if G.identity not in K_elements:
            is_subgroup = False
        else:
            for k1 in K_elements:
                for k2 in K_elements:
                    if k1 * k2 not in K_elements:
                        is_subgroup = False
                        break
                if not is_subgroup: break
                
        if not is_subgroup:
            return [h1_ok, True]
            
        # Check if K is a normal subgroup
        is_normal = True
        for g in G_elements:
            g_inv = ~g
            for k in K_elements:
                if g * k * g_inv not in K_elements:
                    is_normal = False
                    break
            if not is_normal: break
            
        if not is_normal:
            return [h1_ok, True]
            
        # Construct cosets for G/K
        cosets = []
        coset_repr = []
        seen = set()
        for g in G_elements:
            if g not in seen:
                coset = frozenset(g * k for k in K_elements)
                cosets.append(coset)
                coset_repr.append(g)
                seen.update(coset)
                
        m = len(cosets)
        coset_to_idx = {c: i for i, c in enumerate(cosets)}
        
        # Construct regular representation of G/K
        perms = []
        for i in range(m):
            g_i = coset_repr[i]
            perm_array = [0] * m
            for j in range(m):
                g_j = coset_repr[j]
                prod_g = g_i * g_j
                prod_coset = frozenset(prod_g * k for k in K_elements)
                perm_array[j] = coset_to_idx[prod_coset]
            perms.append(Permutation(perm_array))
            
        quotient_group = PermutationGroup(*perms)
        
        # Construct image subgroup phi(G)
        image_elements = list(set(phi_dict.values()))
        image_elements_set = set(image_elements)
        
        # Check if image is a subgroup
        is_img_subgroup = True
        if H_id not in image_elements_set:
            is_img_subgroup = False
        else:
            for y1 in image_elements_set:
                for y2 in image_elements_set:
                    if y1 * y2 not in image_elements_set:
                        is_img_subgroup = False
                        break
                if not is_img_subgroup: break
                
        if not is_img_subgroup:
            return [h1_ok, True]
            
        image_group = PermutationGroup(*image_elements)
        
        # Check isomorphism
        is_iso = quotient_group.is_isomorphic(image_group)
        neg_q_ok = not is_iso
        
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "¬Q: G/ker(phi) is NOT isomorphic to phi(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1