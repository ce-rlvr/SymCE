import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    # Extract witness components. 
    # Support both (G, phi) and (G, G_prime, phi) formats.
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, phi = witness
                try:
                    G_prime = G.derived_subgroup()
                    h2_ok = True
                except Exception:
                    h2_ok = False
            elif len(witness) == 3:
                G, G_prime, phi = witness
                try:
                    h2_ok = (set(G_prime.elements) == set(G.derived_subgroup().elements))
                except Exception:
                    h2_ok = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: phi(G') != G'
    try:
        G_prime_elements = set(G_prime.elements)
        image_G_prime = set()
        
        for g in G_prime_elements:
            if isinstance(phi, dict):
                val = phi[g]
            elif callable(phi):
                val = phi(g)
            elif hasattr(phi, 'apply'):
                val = phi.apply(g)
            else:
                raise ValueError("phi is not a valid mapping")
            image_G_prime.add(val)
            
        neg_q = (image_G_prime != G_prime_elements)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G' is the commutator subgroup of G",
    "¬Q: phi(G') != G'"
]

N_HYP = 2
NEG_Q_INDEX = 2