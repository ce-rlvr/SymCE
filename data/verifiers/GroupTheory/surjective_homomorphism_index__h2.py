import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
import math

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
        G, G_prime, H, phi = witness
    except Exception:
        return [False, False, False, False]

    try:
        if callable(phi):
            phi_func = phi
        elif isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = None
    except Exception:
        phi_func = None

    # H1: G and G_prime are groups, phi is a homomorphism
    try:
        h1 = False
        if phi_func is not None and hasattr(G, "elements") and hasattr(G_prime, "elements"):
            G_elems = list(G.elements)
            G_prime_elems = list(G_prime.elements)
            
            maps_to_G_prime = True
            for g in G_elems:
                if phi_func(g) not in G_prime_elems:
                    maps_to_G_prime = False
                    break
            
            if maps_to_G_prime:
                is_hom = True
                for x in G_elems:
                    for y in G_elems:
                        if phi_func(x * y) != phi_func(x) * phi_func(y):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h1 = is_hom
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = False
        if hasattr(H, "elements") and hasattr(G, "elements"):
            H_elems = list(H.elements)
            G_elems = list(G.elements)
            if all(h in G_elems for h in H_elems):
                if len(H_elems) > 0:
                    is_subgroup = True
                    for a in H_elems:
                        for b in H_elems:
                            if a * b not in H_elems:
                                is_subgroup = False
                                break
                        if not is_subgroup:
                            break
                    h2 = is_subgroup
    except Exception:
        h2 = False

    # H3: The kernel of phi is a subset of H
    try:
        h3 = False
        if phi_func is not None and hasattr(G, "elements") and hasattr(G_prime, "elements") and hasattr(H, "elements"):
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            G_prime_elems = list(G_prime.elements)
            
            id_G_prime = None
            for e in G_prime_elems:
                if e * e == e:
                    id_G_prime = e
                    break
            
            if id_G_prime is not None:
                kernel = [g for g in G_elems if phi_func(g) == id_G_prime]
                h3 = all(k in H_elems for k in kernel)
    except Exception:
        h3 = False

    # neg_Q: [G : H] != [G_prime : phi(H)]
    try:
        neg_q = False
        if phi_func is not None and hasattr(G, "elements") and hasattr(G_prime, "elements") and hasattr(H, "elements"):
            G_elems = list(G.elements)
            H_elems = list(H.elements)
            G_prime_elems = list(G_prime.elements)
            
            if len(H_elems) > 0:
                index_G_H = len(G_elems) / len(H_elems)
                
                phi_H_elements = set(phi_func(h) for h in H_elems)
                order_phi_H = len(phi_H_elements)
                
                if order_phi_H > 0:
                    index_G_prime_phi_H = len(G_prime_elems) / order_phi_H
                    
                    neg_q = abs(index_G_H - index_G_prime_phi_H) > 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and G_prime are groups",
    "H_2: H is a subgroup of G",
    "H_3: The kernel of phi is a subset of H",
    "¬Q: The index of H in G is not equal to the index of phi(H) in G_prime"
]

N_HYP = 3
NEG_Q_INDEX = 3