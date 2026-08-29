import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
        if isinstance(witness, dict):
            G = witness.get('G')
            G_prime = witness.get('G_prime')
            phi = witness.get('phi')
            H = witness.get('H')
        else:
            G, G_prime, phi, H = witness
    except Exception:
        return [False, False, False, False]

    def apply_phi(g):
        if isinstance(phi, dict):
            return phi[g]
        elif callable(phi):
            return phi(g)
        elif isinstance(phi, list):
            for k, v in phi:
                if k == g:
                    return v
            raise ValueError("Mapping not found")
        else:
            raise TypeError("Unsupported phi type")

    def get_elements(group):
        if hasattr(group, 'elements'):
            try:
                elts = list(group.elements)
                if len(elts) > 0:
                    return elts
            except Exception:
                pass
        if hasattr(group, 'generate'):
            return list(group.generate())
        return list(group)

    def get_identity(group):
        if hasattr(group, 'identity'):
            return group.identity
        for e in get_elements(group):
            if e * e == e:
                return e
        return None

    # H1: phi is a surjective group homomorphism from G to G_prime
    h1 = False
    try:
        G_elements = get_elements(G)
        G_prime_elements = get_elements(G_prime)
        
        is_hom = True
        for g1 in G_elements:
            for g2 in G_elements:
                if apply_phi(g1 * g2) != apply_phi(g1) * apply_phi(g2):
                    is_hom = False
                    break
            if not is_hom:
                break
                
        if is_hom:
            image = []
            for g in G_elements:
                val = apply_phi(g)
                if val not in image:
                    image.append(val)
            
            is_surj = True
            for gp in G_prime_elements:
                if gp not in image:
                    is_surj = False
                    break
            if is_surj:
                h1 = True
    except Exception:
        pass

    # H2: H is a subgroup of G
    h2 = False
    try:
        is_sub = None
        if hasattr(H, 'is_subgroup'):
            try:
                is_sub = H.is_subgroup(G)
            except Exception:
                pass
        
        if is_sub is None:
            H_elements = get_elements(H)
            G_elements = get_elements(G)
            
            is_subset = True
            for h_el in H_elements:
                if h_el not in G_elements:
                    is_subset = False
                    break
                    
            if is_subset and len(H_elements) > 0:
                is_sub = True
                for h_el in H_elements:
                    if h_el**-1 not in H_elements:
                        is_sub = False
                        break
                    for h_el2 in H_elements:
                        if h_el * h_el2 not in H_elements:
                            is_sub = False
                            break
                    if not is_sub:
                        break
            else:
                is_sub = False
        h2 = bool(is_sub)
    except Exception:
        pass

    # H3: The kernel of phi is a subset of H
    h3 = False
    try:
        id_G_prime = get_identity(G_prime)
        H_elements = get_elements(H)
        ker_subset = True
        for g in get_elements(G):
            if apply_phi(g) == id_G_prime:
                if g not in H_elements:
                    ker_subset = False
                    break
        h3 = ker_subset
    except Exception:
        pass

    # ¬Q: The index of H in G is not equal to the index of phi(H) in G_prime
    neg_q = False
    try:
        H_elements = get_elements(H)
        phi_H_elements = []
        for h_el in H_elements:
            val = apply_phi(h_el)
            if val not in phi_H_elements:
                phi_H_elements.append(val)
        
        len_G = len(get_elements(G))
        len_H = len(H_elements)
        len_G_prime = len(get_elements(G_prime))
        len_phi_H = len(phi_H_elements)
        
        if len_G * len_phi_H != len_G_prime * len_H:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a surjective group homomorphism from G to G_prime",
    "H_2: H is a subgroup of G",
    "H_3: The kernel of phi is a subset of H",
    "¬Q: The index of H in G is not equal to the index of phi(H) in G_prime"
]

N_HYP = 3
NEG_Q_INDEX = 3