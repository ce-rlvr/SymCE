import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def apply_phi(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    elif callable(phi):
        return phi(x)
    elif hasattr(phi, 'image'):
        return phi.image(x)
    elif hasattr(phi, '__mul__') and hasattr(phi, '__pow__'):
        # If phi is provided as an element of G, assume conjugation by phi
        return phi * x * phi**-1
    else:
        raise ValueError("Unknown phi format")

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, phi = witness
        else:
            G = witness.G
            phi = witness.phi
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: phi is an inner automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.elements)
            
            # Check bijection
            mapped = [apply_phi(phi, x) for x in elements]
            is_bijection = len(set(mapped)) == len(elements) and all(y in elements for y in mapped)
            
            # Check homomorphism
            is_hom = True
            for x in elements:
                for y in elements:
                    if apply_phi(phi, x * y) != apply_phi(phi, x) * apply_phi(phi, y):
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
            is_auto = is_bijection and is_hom
            
            # Check inner
            is_inner = False
            if is_auto:
                for g in elements:
                    g_inv = g**-1
                    if all(apply_phi(phi, x) == g * x * g_inv for x in elements):
                        is_inner = True
                        break
            h2 = is_inner
    except Exception:
        h2 = False
        
    # H3: bar_phi is the induced automorphism defined by bar_phi(xG') = phi(x)G'
    # We verify that phi preserves the derived subgroup G' so that bar_phi is well-defined.
    try:
        if not h1:
            h3 = False
        else:
            G_prime = G.derived_subgroup()
            gp_elements = list(G_prime.elements)
            is_well_defined = True
            for x in gp_elements:
                if apply_phi(phi, x) not in gp_elements:
                    is_well_defined = False
                    break
            h3 = is_well_defined
    except Exception:
        h3 = False
        
    # neg_Q: bar_phi is NOT the identity map on G/G'
    try:
        if not h1:
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            gp_elements = list(G_prime.elements)
            is_identity = True
            for x in list(G.elements):
                # x G' == phi(x) G' iff x^-1 * phi(x) is in G'
                val = x**-1 * apply_phi(phi, x)
                if val not in gp_elements:
                    is_identity = False
                    break
            neg_q = not is_identity
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an inner automorphism of G",
    "H_3: bar_phi is the induced automorphism on G/G'",
    "¬Q: bar_phi is not the identity map on G/G'"
]

N_HYP = 3
NEG_Q_INDEX = 3