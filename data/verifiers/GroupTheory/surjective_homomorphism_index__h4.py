import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            G_prime = witness.get('G_prime')
            phi = witness.get('phi')
            H = witness.get('H')
        else:
            G, G_prime, phi, H = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(G_prime, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1:
            elements_G = list(G.generate())
            elements_G_prime = list(G_prime.generate())
            
            norm_phi = {}
            if callable(phi):
                for eg in elements_G:
                    norm_phi[eg] = phi(eg)
            elif isinstance(phi, dict):
                for eg in elements_G:
                    if eg in phi:
                        norm_phi[eg] = phi[eg]
                    else:
                        for k, v in phi.items():
                            if k == eg:
                                norm_phi[eg] = v
                                break
    except Exception:
        pass

    try:
        if h1 and len(norm_phi) == len(elements_G):
            images = [norm_phi[eg] for eg in elements_G]
            is_homo = True
            for g1 in elements_G:
                val_g1 = norm_phi[g1]
                for g2 in elements_G:
                    prod = g1 * g2
                    val_prod = None
                    for i, eg in enumerate(elements_G):
                        if eg == prod:
                            val_prod = images[i]
                            break
                    
                    val_g2 = norm_phi[g2]
                    
                    if val_prod != val_g1 * val_g2:
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            if is_homo:
                image_elements = []
                for v in images:
                    if not any(v == iv for iv in image_elements):
                        image_elements.append(v)
                
                is_surj = True
                for egp in elements_G_prime:
                    if not any(egp == iv for iv in image_elements):
                        is_surj = False
                        break
                
                if is_surj:
                    for iv in image_elements:
                        if not any(iv == egp for egp in elements_G_prime):
                            is_surj = False
                            break
                h2 = is_surj
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            if isinstance(H, PermutationGroup):
                h3 = True
                for g in H.generators:
                    if not any(g == eg for eg in elements_G):
                        h3 = False
                        break
                H_group = H
            elif isinstance(H, (list, set, tuple)):
                H_list = list(H)
                h3 = True
                for g in H_list:
                    if not any(g == eg for eg in elements_G):
                        h3 = False
                        break
                if h3 and H_list:
                    for g1 in H_list:
                        for g2 in H_list:
                            prod = g1 * g2
                            if not any(prod == h for h in H_list):
                                h3 = False
                                break
                        if not h3:
                            break
                if not H_list:
                    for eg in elements_G:
                        if eg * eg == eg:
                            H_list = [eg]
                            break
                H_group = PermutationGroup(H_list)
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if h1 and h3 and len(norm_phi) == len(elements_G):
            index_G_H = G.order() // H_group.order()
            
            phi_H_gens = []
            for g in H_group.generators:
                for eg in elements_G:
                    if g == eg:
                        phi_H_gens.append(norm_phi[eg])
                        break
                        
            if not phi_H_gens:
                for egp in elements_G_prime:
                    if egp * egp == egp:
                        phi_H_gens = [egp]
                        break
                
            phi_H_group = PermutationGroup(phi_H_gens)
            index_G_prime_phi_H = G_prime.order() // phi_H_group.order()
            
            neg_q = index_G_H != index_G_prime_phi_H
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and G_prime are groups",
    "H_2: phi is a surjective group homomorphism from G to G_prime",
    "H_3: H is a subgroup of G",
    "¬Q: The index of H in G is not equal to the index of phi(H) in G_prime"
]

N_HYP = 3
NEG_Q_INDEX = 3