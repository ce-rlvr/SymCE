import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard group theory and linear algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def make_hashable(elem):
    """Convert mutable sympy objects (like Matrix) to immutable ones for set operations."""
    if hasattr(elem, 'as_immutable'):
        return elem.as_immutable()
    return elem

def get_elements(grp):
    """Extract all elements from a group or iterable into a set of hashable objects."""
    if isinstance(grp, (set, list, tuple)):
        elems = grp
    elif hasattr(grp, 'generate'):
        elems = grp.generate()
    elif hasattr(grp, 'elements'):
        elems = grp.elements
    else:
        elems = grp
    
    res = set()
    for e in elems:
        res.add(make_hashable(e))
    return res

def conditions(witness) -> list[bool]:
    try:
        # Witness can be (G, N, H) or (G, N, H, C_N_H, Z_H)
        if len(witness) == 3:
            G, N, H = witness
            C_N_H_given = None
            Z_H_given = None
        elif len(witness) == 5:
            G, N, H, C_N_H_given, Z_H_given = witness
        else:
            return [False, False, False, False]
            
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        # H_1: G is an internal semidirect product of a normal subgroup N and a subgroup H
        h1 = True
        if not N_elems.issubset(G_elems):
            h1 = False
        elif not H_elems.issubset(G_elems):
            h1 = False
        else:
            is_norm = True
            for n in N_elems:
                for g in G_elems:
                    conj = make_hashable(g * n * g**-1)
                    if conj not in N_elems:
                        is_norm = False
                        break
                if not is_norm:
                    break
            if not is_norm:
                h1 = False
            elif len(N_elems.intersection(H_elems)) != 1:
                h1 = False
            elif len(N_elems) * len(H_elems) != len(G_elems):
                h1 = False
    except Exception:
        h1 = False

    try:
        # H_2: C_N(H) is the centralizer of H in N
        C_N_H = set()
        for n in N_elems:
            commutes = True
            for h in H_elems:
                if make_hashable(n * h) != make_hashable(h * n):
                    commutes = False
                    break
            if commutes:
                C_N_H.add(n)
        
        if C_N_H_given is not None:
            h2 = (C_N_H == get_elements(C_N_H_given))
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        # H_3: Z(H) is the center of H
        Z_H = set()
        for h1_elem in H_elems:
            commutes = True
            for h2_elem in H_elems:
                if make_hashable(h1_elem * h2_elem) != make_hashable(h2_elem * h1_elem):
                    commutes = False
                    break
            if commutes:
                Z_H.add(h1_elem)
                
        if Z_H_given is not None:
            h3 = (Z_H == get_elements(Z_H_given))
        else:
            h3 = True
    except Exception:
        h3 = False

    try:
        # ¬Q: C_G(H) is NOT equal to the internal direct product C_N(H) x Z(H)
        C_G_H = set()
        for g in G_elems:
            commutes = True
            for h in H_elems:
                if make_hashable(g * h) != make_hashable(h * g):
                    commutes = False
                    break
            if commutes:
                C_G_H.add(g)
        
        # The internal direct product of C_N(H) and Z(H) is the set of their products
        # (since they intersect trivially and commute element-wise)
        prod_set = set()
        for n in C_N_H:
            for z in Z_H:
                prod_set.add(make_hashable(n * z))
        
        neg_q = (C_G_H != prod_set)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is an internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: C_N(H) is the centralizer of H in N",
    "H_3: Z(H) is the center of H",
    "¬Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3