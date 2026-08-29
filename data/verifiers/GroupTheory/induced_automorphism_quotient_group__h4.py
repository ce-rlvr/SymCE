import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, N, phi_dict = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            G_elements = set(G.generate())
            is_sub = all(gen in G_elements for gen in N.generators)
            if is_sub:
                h2 = bool(N.is_normal(G))
    except Exception:
        h2 = False
        
    # H3: \phi is an automorphism of G
    try:
        h3 = False
        elements = list(G.generate())
        if callable(phi_dict):
            phi = phi_dict
        elif isinstance(phi_dict, dict):
            phi = lambda x: phi_dict[x]
        else:
            phi = None
            
        if phi is not None:
            mapped_elements = [phi(x) for x in elements]
            if len(set(mapped_elements)) == len(elements) and set(mapped_elements) == set(elements):
                is_hom = True
                for x in elements:
                    for y in elements:
                        if phi(x * y) != phi(x) * phi(y):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                h3 = is_hom
    except Exception:
        h3 = False
        
    # neg_Q: \bar{\phi} is NOT an automorphism of G/N
    try:
        neg_q = False
        elements = list(G.generate())
        N_elements = set(N.generate())
        
        if callable(phi_dict):
            phi = phi_dict
        elif isinstance(phi_dict, dict):
            phi = lambda x: phi_dict[x]
        else:
            raise ValueError("phi is neither callable nor dict")
            
        is_auto = True
        
        # Check well-definedness
        for x in elements:
            for y in elements:
                if (~x * y) in N_elements:
                    if (~phi(x) * phi(y)) not in N_elements:
                        is_auto = False
                        break
            if not is_auto:
                break
                
        if is_auto:
            # Check homomorphism
            for x in elements:
                for y in elements:
                    if (~(phi(x) * phi(y)) * phi(x * y)) not in N_elements:
                        is_auto = False
                        break
                if not is_auto:
                    break

        if is_auto:
            # Check bijection
            cosets = []
            for x in elements:
                coset = frozenset([x * n for n in N_elements])
                if coset not in cosets:
                    cosets.append(coset)
                    
            mapped_cosets = set()
            for c in cosets:
                rep = next(iter(c))
                mapped_rep = phi(rep)
                mapped_coset = frozenset([mapped_rep * n for n in N_elements])
                mapped_cosets.add(mapped_coset)
                
            if len(mapped_cosets) != len(cosets):
                is_auto = False
                
        neg_q = not is_auto
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: \\phi is an automorphism of G",
    "¬Q: \\bar{\\phi} is not an automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3