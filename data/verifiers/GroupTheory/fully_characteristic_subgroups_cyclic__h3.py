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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H, phi), check the remaining hypotheses and the negated conclusion.
    """
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a cyclic group
    try:
        h1_ok = bool(G.is_cyclic)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = bool(H.is_subgroup(G))
    except Exception:
        h2_ok = False

    # ¬Q: \phi(H) \not\subseteq H
    try:
        subset = True
        
        # Normalize phi to be callable or a dictionary
        if not callable(phi) and not isinstance(phi, dict):
            try:
                phi_dict = dict(phi)
            except Exception:
                phi_dict = phi
        else:
            phi_dict = phi

        h_elements = H.elements
        for h in h_elements:
            if callable(phi_dict):
                mapped_h = phi_dict(h)
            else:
                mapped_h = phi_dict[h]
            
            if mapped_h not in h_elements:
                subset = False
                break
                
        neg_q_ok = not subset
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: H is a subgroup of G",
    "¬Q: phi(H) is not a subset of H"
]

N_HYP = 2
NEG_Q_INDEX = 2