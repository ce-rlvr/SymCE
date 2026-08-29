import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def eval_phi(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    return phi(x)

def get_elements(group):
    if hasattr(group, 'elements'):
        try:
            res = list(group.elements)
            if len(res) > 0: 
                return res
        except Exception:
            pass
    if hasattr(group, 'generate_dimino'):
        return list(group.generate_dimino())
    if hasattr(group, 'generate'):
        return list(group.generate())
    return list(group)

def is_subgroup(H, G):
    try:
        if hasattr(H, 'is_subgroup'):
            return H.is_subgroup(G)
    except Exception:
        pass
    return all(G.contains(g) for g in H.generators)

def is_normal(H, G):
    try:
        if hasattr(H, 'is_normal'):
            return H.is_normal(G)
    except Exception:
        pass
    return all(H.contains(g * h * ~g) for g in G.generators for h in H.generators)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and is_subgroup(N, G) and is_normal(N, G)
    except Exception:
        h2 = False

    # H_3: \phi(N) = N
    try:
        N_elements = get_elements(N)
        phi_N = {eval_phi(phi, x) for x in N_elements}
        h3 = phi_N == set(N_elements)
    except Exception:
        h3 = False

    # ¬Q: \bar{\phi} is NOT an automorphism of G/N
    try:
        G_elements = get_elements(G)
        N_elements = get_elements(N)
        
        def coset(x):
            return frozenset(x * n for n in N_elements)
            
        is_automorphism = True
        
        # Check if phi maps G to G
        for x in G_elements:
            if not G.contains(eval_phi(phi, x)):
                is_automorphism = False
                break
        
        if is_automorphism:
            # Check well-definedness
            well_defined = True
            for x in G_elements:
                for n in N_elements:
                    if coset(eval_phi(phi, x * n)) != coset(eval_phi(phi, x)):
                        well_defined = False
                        break
                if not well_defined:
                    break
            is_automorphism = is_automorphism and well_defined
            
        if is_automorphism:
            # Check homomorphism property
            is_homo = True
            for x in G_elements:
                for y in G_elements:
                    if coset(eval_phi(phi, x * y)) != coset(eval_phi(phi, x) * eval_phi(phi, y)):
                        is_homo = False
                        break
                if not is_homo:
                    break
            is_automorphism = is_automorphism and is_homo
            
        if is_automorphism:
            # Check bijection
            domain_cosets = set(coset(x) for x in G_elements)
            image_cosets = set(coset(eval_phi(phi, x)) for x in G_elements)
            if len(image_cosets) != len(domain_cosets):
                is_automorphism = False
                
        neg_q = not is_automorphism
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: \\phi(N) = N",
    "¬Q: \\bar{\\phi} is not an automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3