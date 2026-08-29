import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: G and G_prime are groups",
    "H_2: phi is a surjective group homomorphism from G to G_prime",
    "H_3: The kernel of phi is a subset of H",
    "¬Q: The index of H in G is not equal to the index of phi(H) in G_prime"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, G_prime, phi, H_elements = witness
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = phi
    except Exception:
        phi_func = None

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(G_prime, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1 and phi_func is not None:
            G_elements = list(G.elements)
            G_prime_elements = list(G_prime.elements)
            
            is_homo = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                        is_homo = False
                        break
                if not is_homo:
                    break
            
            images = set(phi_func(g) for g in G_elements)
            is_surj = len(images) == len(G_prime_elements) and all(img in G_prime_elements for img in images)
            
            h2 = is_homo and is_surj
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            G_elements = list(G.elements)
            id_prime = G_prime.identity
            kernel = set(g for g in G_elements if phi_func(g) == id_prime)
            
            if isinstance(H_elements, PermutationGroup):
                H_set = set(H_elements.elements)
            else:
                H_set = set(H_elements)
                
            is_subgroup = True
            id_G = G.identity
            if id_G not in H_set:
                is_subgroup = False
            else:
                for h_a in H_set:
                    for h_b in H_set:
                        if (h_a * h_b) not in H_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                if is_subgroup:
                    for h_a in H_set:
                        if (h_a**-1) not in H_set:
                            is_subgroup = False
                            break
            
            h3 = kernel.issubset(H_set) and H_set.issubset(set(G_elements)) and is_subgroup
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if h1 and h2 and h3:
            G_elements = list(G.elements)
            G_prime_elements = list(G_prime.elements)
            
            if isinstance(H_elements, PermutationGroup):
                H_set = set(H_elements.elements)
            else:
                H_set = set(H_elements)
            
            phi_H = set(phi_func(h) for h in H_set)
            
            neg_q = (len(G_elements) * len(phi_H)) != (len(G_prime_elements) * len(H_set))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]