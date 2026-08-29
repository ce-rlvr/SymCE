import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
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

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, phi = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.generate())
            if isinstance(phi, dict):
                mapping = phi
            else:
                mapping = {g: phi(g) for g in elements}
            
            domain = set(mapping.keys())
            image = set(mapping.values())
            
            if domain != set(elements) or image != set(elements):
                h2 = False
            else:
                h2 = True
                for x in elements:
                    for y in elements:
                        if mapping[x * y] != mapping[x] * mapping[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # neg_Q: phi(G') != G'
    try:
        if not h1:
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            G_prime_elements = set(G_prime.generate())
            
            if isinstance(phi, dict):
                phi_G_prime = set(phi[g] for g in G_prime_elements)
            else:
                phi_G_prime = set(phi(g) for g in G_prime_elements)
                
            neg_q = (phi_G_prime != G_prime_elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(G') != G'"
]

N_HYP = 2
NEG_Q_INDEX = 2