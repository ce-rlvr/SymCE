import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: phi is a map from G to H
    try:
        try:
            G_elements = set(G.elements)
        except Exception:
            G_elements = set(G.generate())
            
        try:
            H_elements = set(H.elements)
        except Exception:
            H_elements = set(H.generate())
            
        if isinstance(phi, dict):
            phi_dict = phi
        elif isinstance(phi, (list, tuple, set)):
            phi_dict = dict(phi)
        else:
            phi_dict = None

        if phi_dict is not None:
            h3 = set(phi_dict.keys()) == G_elements and all(v in H_elements for v in phi_dict.values())
            image = set(phi_dict.values())
        elif callable(phi):
            image = set()
            h3 = True
            for g in G_elements:
                v = phi(g)
                if v not in H_elements:
                    h3 = False
                    break
                image.add(v)
        else:
            h3 = False
            image = set()
    except Exception:
        h3 = False
        image = set()

    # ¬Q: phi(G) is NOT a subgroup of H
    try:
        if not h3:
            neg_q = False
        else:
            is_subgroup = True
            if not image:
                is_subgroup = False
            else:
                for a in image:
                    if ~a not in image:
                        is_subgroup = False
                        break
                    for b in image:
                        if a * b not in image:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a group",
    "H_3: phi is a map from G to H",
    "¬Q: phi(G) is not a subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3