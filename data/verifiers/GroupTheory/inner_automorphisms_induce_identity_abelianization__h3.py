import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
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

def get_phi_x(phi, x):
    if isinstance(phi, dict):
        return phi[x]
    return phi(x)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (G, phi) where G is a PermutationGroup
    and phi is a callable or dictionary mapping elements of G to elements of G.
    """
    try:
        G, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G' is the commutator subgroup of G
    # This is definitional; if G is a group, we can compute its commutator subgroup.
    h2 = h1

    # H3: \bar{\phi} is the induced automorphism on G/G'
    try:
        if not h1:
            h3 = False
        else:
            G_prime = G.derived_subgroup()
            elements = list(G.elements)
            
            maps_to_G = True
            for x in elements:
                if get_phi_x(phi, x) not in G:
                    maps_to_G = False
                    break
            
            if not maps_to_G:
                h3 = False
            else:
                is_well_defined = True
                is_hom = True
                
                for x in elements:
                    px = get_phi_x(phi, x)
                    for y in elements:
                        py = get_phi_x(phi, y)
                        
                        # well-defined: x * y^-1 in G' => px * py^-1 in G'
                        if (x * (~y)) in G_prime:
                            if (px * (~py)) not in G_prime:
                                is_well_defined = False
                                break
                        
                        # homomorphism: phi(x*y) * (px * py)^-1 in G'
                        pxy = get_phi_x(phi, x * y)
                        if (pxy * (~(px * py))) not in G_prime:
                            is_hom = False
                            break
                    if not is_well_defined or not is_hom:
                        break
                
                is_surj = True
                if is_well_defined and is_hom:
                    for y in elements:
                        found = False
                        for x in elements:
                            px = get_phi_x(phi, x)
                            if (px * (~y)) in G_prime:
                                found = True
                                break
                        if not found:
                            is_surj = False
                            break
                
                h3 = is_well_defined and is_hom and is_surj
    except Exception:
        h3 = False

    # ¬Q: \bar{\phi} is NOT the identity map on G/G'
    try:
        if not (h1 and h3):
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            neg_q = False
            for x in G.elements:
                px = get_phi_x(phi, x)
                # \bar{\phi}(xG') != xG' iff x^{-1} * \phi(x) not in G'
                if ((~x) * px) not in G_prime:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: G is a group",
    r"H_2: G' is the commutator subgroup of G",
    r"H_3: \bar{\phi} is the induced automorphism on G/G'",
    r"¬Q: \bar{\phi} is not the identity map on G/G'"
]

N_HYP = 3
NEG_Q_INDEX = 3