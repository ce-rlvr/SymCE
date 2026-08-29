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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_phi_g(phi, g):
    """Helper to evaluate the homomorphism/automorphism."""
    if isinstance(phi, dict):
        return phi[g]
    return phi(g)

def conditions(witness) -> list[bool]:
    try:
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]

    # H_1: Let N be a normal subgroup of G
    try:
        h1 = N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h1 = False

    # H_2: Let \phi be an automorphism of G
    try:
        elements = list(G.elements)
        mapped = []
        is_hom = True
        for g in elements:
            mg = get_phi_g(phi, g)
            if mg not in G:
                is_hom = False
                break
            mapped.append(mg)
        
        # Check bijection and homomorphism properties
        if is_hom and len(set(mapped)) == len(elements):
            for g1 in elements:
                for g2 in elements:
                    if get_phi_g(phi, g1 * g2) != get_phi_g(phi, g1) * get_phi_g(phi, g2):
                        is_hom = False
                        break
                if not is_hom:
                    break
            h2 = is_hom
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: \phi(N) = N (i.e., N is invariant under \phi)
    try:
        n_elements = list(N.elements)
        mapped_n = set()
        for n in n_elements:
            mapped_n.add(get_phi_g(phi, n))
        h3 = (mapped_n == set(n_elements))
    except Exception:
        h3 = False

    # neg_Q: The map \bar{\phi}: G/N \to G/N is NOT a well-defined automorphism of G/N
    try:
        # For finite groups, \bar{\phi} is a well-defined automorphism if and only if \phi(N) == N.
        # If \phi(N) != N, it is either not well-defined or not surjective/injective.
        n_elements = list(N.elements)
        mapped_n = set()
        for n in n_elements:
            mapped_n.add(get_phi_g(phi, n))
        
        is_well_defined_automorphism = (mapped_n == set(n_elements))
        neg_q = not is_well_defined_automorphism
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: phi is an automorphism of G",
    "H_3: phi(N) = N (i.e., N is invariant under phi)",
    "¬Q: bar{phi} is not a well-defined automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3