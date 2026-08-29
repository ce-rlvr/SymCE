import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: N is a finite group",
    "H_2: G is the semidirect product of N and H",
    "¬Q: It is NOT the case that (G is nilpotent iff the semidirect product is a direct product and both N and H are nilpotent)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_order(grp):
    val = grp.order
    if callable(val):
        return val()
    return val

def get_elements(grp):
    try:
        return set(grp.generate())
    except Exception:
        return set(grp.elements)

def get_is_nilpotent(grp):
    val = grp.is_nilpotent
    if callable(val):
        return val()
    return val

def conditions(witness):
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            G = witness['G']
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            N, H, G = witness
            if get_order(G) < get_order(N) or get_order(G) < get_order(H):
                if get_order(witness[0]) >= get_order(witness[1]) and get_order(witness[0]) >= get_order(witness[2]):
                    G = witness[0]
                    N = witness[1]
                    H = witness[2]
            
            def check_norm(sub, super_grp):
                try:
                    for g in super_grp.generators:
                        g_inv = ~g
                        for n in sub.generators:
                            if (g * n * g_inv) not in sub:
                                return False
                    return True
                except Exception:
                    return False
            
            if not check_norm(N, G) and check_norm(H, G):
                N, H = H, N
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: N is a finite group
    try:
        h1 = isinstance(N, PermutationGroup) and get_order(N) < float('inf')
    except Exception:
        h1 = False

    # H_2: G is the semidirect product of N and H
    try:
        n_sub = all(g in G for g in N.generators)
        h_sub = all(g in G for g in H.generators)
        
        n_normal = True
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if (g * n * g_inv) not in N:
                    n_normal = False
                    break
            if not n_normal:
                break
                
        n_elems = get_elements(N)
        h_elems = get_elements(H)
        trivial_intersect = len(n_elems.intersection(h_elems)) == 1
        
        order_ok = (get_order(N) * get_order(H) == get_order(G))
        
        h2 = bool(n_sub and h_sub and n_normal and trivial_intersect and order_ok)
    except Exception:
        h2 = False

    # neg_Q: G is nilpotent iff the semidirect product is a direct product and both N and H are nilpotent groups
    try:
        g_nilp = bool(get_is_nilpotent(G))
        n_nilp = bool(get_is_nilpotent(N))
        h_nilp = bool(get_is_nilpotent(H))
        
        commute = True
        for n in N.generators:
            for h in H.generators:
                if n * h != h * n:
                    commute = False
                    break
            if not commute:
                break
        is_direct = commute
        
        q = (is_direct and n_nilp and h_nilp)
        neg_q = (g_nilp != q)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]