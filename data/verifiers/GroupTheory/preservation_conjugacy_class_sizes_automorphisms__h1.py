import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    """Helper to extract elements from a group."""
    if hasattr(G, "generate") and callable(G.generate):
        return list(G.generate())
    elif hasattr(G, "elements"):
        return list(G.elements)
    else:
        return list(G)

def conditions(witness) -> list[bool]:
    try:
        G, phi, x = witness
    except Exception:
        return [False, False, False]

    # H_1: phi is an automorphism of G
    try:
        elements = get_elements(G)
        if callable(phi):
            phi_map = {g: phi(g) for g in elements}
        elif isinstance(phi, dict):
            phi_map = {g: phi[g] for g in elements}
        else:
            phi_map = None

        if phi_map is None:
            h1 = False
        else:
            # Check if all images are in G
            if not all(v in elements for v in phi_map.values()):
                h1 = False
            # Check if it is a bijection
            elif len(set(phi_map.values())) != len(elements):
                h1 = False
            else:
                # Check homomorphism property: phi(a * b) == phi(a) * phi(b)
                h1 = True
                for a in elements:
                    for b in elements:
                        if phi_map[a * b] != phi_map[a] * phi_map[b]:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        elements = get_elements(G)
        h2 = x in elements
    except Exception:
        h2 = False

    # ¬Q: The cardinality of the conjugacy class of x in G is NOT equal to the cardinality of the conjugacy class of phi(x) in G
    try:
        if callable(phi):
            phi_x = phi(x)
        elif isinstance(phi, dict):
            phi_x = phi[x]
        else:
            phi_x = None

        if phi_x is None:
            neg_q = False
        else:
            elements = get_elements(G)
            # Conjugacy class of x: {g * x * g^-1 | g \in G}
            conj_x = set(g * x * g**-1 for g in elements)
            # Conjugacy class of phi(x): {g * phi(x) * g^-1 | g \in G}
            conj_phi_x = set(g * phi_x * g**-1 for g in elements)
            
            neg_q = len(conj_x) != len(conj_phi_x)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is an automorphism of G",
    "H_2: x is an element of G",
    "¬Q: The cardinality of the conjugacy class of x in G is not equal to the cardinality of the conjugacy class of phi(x) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2