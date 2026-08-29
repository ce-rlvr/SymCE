import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: phi is an automorphism of G",
    "H_3: N is a subgroup of G and phi(N) = N",
    "¬Q: G/N is not a well-defined quotient group (N is not normal in G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def _get_elements(H):
    if isinstance(H, PermutationGroup):
        return set(H.generate())
    else:
        return set(H)

def _is_subgroup(H, G):
    try:
        H_set = _get_elements(H)
        G_set = set(G.generate())
        if not H_set.issubset(G_set):
            return False
        if len(H_set) == 0:
            return False
        for x in H_set:
            if x**-1 not in H_set:
                return False
            for y in H_set:
                if x * y not in H_set:
                    return False
        return True
    except Exception:
        return False

def _is_normal(H, G):
    try:
        H_set = _get_elements(H)
        for g in G.generate():
            g_inv = g**-1
            for h in H_set:
                if g * h * g_inv not in H_set:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, phi, N = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2
    try:
        h2 = False
        if h1:
            G_elems = list(G.generate())
            G_set = set(G_elems)
            
            if callable(phi):
                phi_dict = {x: phi(x) for x in G_elems}
            elif isinstance(phi, dict):
                phi_dict = phi
            else:
                phi_dict = {}
                
            if len(phi_dict) == len(G_set):
                keys_set = set(phi_dict.keys())
                vals_set = set(phi_dict.values())
                if keys_set == G_set and vals_set == G_set:
                    is_hom = True
                    for x in G_elems:
                        for y in G_elems:
                            if phi_dict[x * y] != phi_dict[x] * phi_dict[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    h2 = is_hom
    except Exception:
        h2 = False
        
    # H_3
    try:
        h3 = False
        if h1 and _is_subgroup(N, G):
            N_elems = list(_get_elements(N))
            if callable(phi):
                mapped_N = {phi(x) for x in N_elems}
            elif isinstance(phi, dict):
                mapped_N = {phi.get(x) for x in N_elems}
            else:
                mapped_N = set()
            if mapped_N == set(N_elems):
                h3 = True
    except Exception:
        h3 = False
        
    # neg_Q
    try:
        neg_q = False
        if h1 and _is_subgroup(N, G):
            neg_q = not _is_normal(N, G)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]