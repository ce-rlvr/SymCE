import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

# Top-level setup for potential witness expressions
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

def get_elements(G):
    if hasattr(G, 'elements'):
        if callable(G.elements):
            return list(G.elements())
        return list(G.elements)
    if hasattr(G, 'generate'):
        return list(G.generate())
    return list(G)

def get_identity(G, elements):
    if hasattr(G, 'identity'):
        if callable(G.identity):
            return G.identity()
        return G.identity
    if hasattr(G, 'id'):
        return G.id
    for e in elements:
        if all(e * g == g and g * e == g for g in elements):
            return e
    return None

def apply_phi(phi, g):
    if callable(phi):
        return phi(g)
    return phi[g]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, phi = witness
        else:
            G = witness
            phi = witness.phi
    except Exception:
        return [False, False, False, False]

    # H_1: phi is an automorphism of G
    try:
        if hasattr(G, 'is_automorphism'):
            try:
                h1 = bool(G.is_automorphism())
            except TypeError:
                h1 = bool(G.is_automorphism(phi))
        else:
            elements = get_elements(G)
            mapped = [apply_phi(phi, g) for g in elements]
            h1 = len(set(mapped)) == len(elements) and all(m in elements for m in mapped)
            if h1:
                for g1 in elements:
                    for g2 in elements:
                        if apply_phi(phi, g1 * g2) != apply_phi(phi, g1) * apply_phi(phi, g2):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: The order of phi is 2
    try:
        if hasattr(G, 'phi_order'):
            try:
                h2 = G.phi_order() == 2
            except TypeError:
                h2 = G.phi_order(phi) == 2
        else:
            elements = get_elements(G)
            h2 = True
            is_identity = True
            for g in elements:
                if apply_phi(phi, apply_phi(phi, g)) != g:
                    h2 = False
                    break
                if apply_phi(phi, g) != g:
                    is_identity = False
            if is_identity:
                h2 = False
    except Exception:
        h2 = False

    # H_3: For all g in G, phi(g) = g implies g is the identity element
    try:
        if hasattr(G, 'is_fixed_point_free'):
            try:
                h3 = bool(G.is_fixed_point_free())
            except TypeError:
                h3 = bool(G.is_fixed_point_free(phi))
        else:
            elements = get_elements(G)
            identity = get_identity(G, elements)
            h3 = True
            for g in elements:
                if apply_phi(phi, g) == g and g != identity:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # neg_Q: G is NOT a solvable group
    try:
        if hasattr(G, 'is_solvable'):
            val = G.is_solvable() if callable(G.is_solvable) else G.is_solvable
            neg_q = not bool(val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    r"H_1: \phi is an automorphism of G",
    r"H_2: The order of \phi is 2",
    r"H_3: For all g \in G, \phi(g) = g implies g is the identity element",
    r"¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3