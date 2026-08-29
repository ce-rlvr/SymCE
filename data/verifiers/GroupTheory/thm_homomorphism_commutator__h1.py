import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(group):
    if hasattr(group, 'elements'):
        return list(group.elements)
    return list(group)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi, x, y = witness
    except Exception:
        return [False, False, False]
        
    # H_1: phi is a group homomorphism from G to H
    try:
        h1 = False
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        
        if isinstance(phi, dict):
            mapping = phi
        else:
            mapping = {g: phi(g) for g in G_elems}
            
        if all(mapping.get(g) in H_elems for g in G_elems):
            h1 = all(mapping[a * b] == mapping[a] * mapping[b] for a in G_elems for b in G_elems)
    except Exception:
        h1 = False
        
    # H_2: x and y are elements of G
    try:
        h2 = False
        G_elems = get_elements(G)
        h2 = (x in G_elems) and (y in G_elems)
    except Exception:
        h2 = False
        
    # not Q: phi(commutator(x, y)) != commutator(phi(x), phi(y))
    try:
        neg_q = False
        if isinstance(phi, dict):
            get_phi = lambda g: phi[g]
        else:
            get_phi = phi
            
        # Commutator definition: [a, b] = a * b * a^-1 * b^-1
        comm_xy = x * y * x**-1 * y**-1
        phi_comm = get_phi(comm_xy)
        
        phi_x = get_phi(x)
        phi_y = get_phi(y)
        comm_phi = phi_x * phi_y * phi_x**-1 * phi_y**-1
        
        neg_q = bool(phi_comm != comm_phi)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: x and y are elements of G",
    "not Q: phi(commutator(x, y)) != commutator(phi(x), phi(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2