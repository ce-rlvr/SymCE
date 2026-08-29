import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
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
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(Z(G)) is not equal to Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.generate())
            
            def apply_phi(x):
                if isinstance(phi, dict):
                    return phi[x]
                return phi(x)
            
            images = []
            valid_mapping = True
            for x in elements:
                try:
                    img = apply_phi(x)
                    if img not in elements:
                        valid_mapping = False
                        break
                    images.append(img)
                except Exception:
                    valid_mapping = False
                    break
            
            if not valid_mapping:
                h2 = False
            elif len(set(images)) != len(elements):
                h2 = False
            else:
                h2 = all(apply_phi(a * b) == apply_phi(a) * apply_phi(b) for a in elements for b in elements)
    except Exception:
        h2 = False
        
    # ¬Q: phi(Z(G)) is not equal to Z(G)
    try:
        if not h1:
            neg_q = False
        else:
            center_group = G.center()
            center_elements = list(center_group.generate())
            
            def apply_phi(x):
                if isinstance(phi, dict):
                    return phi[x]
                return phi(x)
            
            phi_center = set()
            for x in center_elements:
                phi_center.add(apply_phi(x))
                
            neg_q = phi_center != set(center_elements)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]