import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_elements(grp):
    if hasattr(grp, 'elements'):
        return set(grp.elements)
    elif hasattr(grp, 'generate'):
        return set(grp.generate())
    else:
        return set(grp)

def inv(a):
    try:
        return a**-1
    except Exception:
        return ~a

def is_subgroup(elems):
    if not elems: 
        return False
    for a in elems:
        if inv(a) not in elems:
            return False
        for b in elems:
            if a * b not in elems:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False]

    try:
        h1 = True
        G_elems = get_elements(G)
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        if not is_subgroup(G_elems):
            h1 = False
        elif not is_subgroup(N_elems):
            h1 = False
        elif not is_subgroup(H_elems):
            h1 = False
        elif not N_elems.issubset(G_elems):
            h1 = False
        elif not H_elems.issubset(G_elems):
            h1 = False
        else:
            is_normal = True
            for g in G_elems:
                for n in N_elems:
                    if g * n * inv(g) not in N_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
            if not is_normal:
                h1 = False
            else:
                intersect = N_elems.intersection(H_elems)
                if len(intersect) != 1:
                    h1 = False
                else:
                    e = list(intersect)[0]
                    if e * e != e:
                        h1 = False
                    elif len(N_elems) * len(H_elems) != len(G_elems):
                        h1 = False
    except Exception:
        h1 = False

    try:
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        # C_N(H) is the centralizer of H in N
        C_N_H = set()
        for n in N_elems:
            if all(n * h == h * n for h in H_elems):
                C_N_H.add(n)
                
        q = True
        for n in N_elems:
            in_C = n in C_N_H
            cond = all(h * n * inv(h) == n for h in H_elems)
            if in_C != cond:
                q = False
                break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is an internal semidirect product of a normal subgroup N and a subgroup H",
    "¬Q: It is not the case that an element n in N belongs to C_N(H) iff hnh^{-1} = n for all h in H"
]

N_HYP = 1
NEG_Q_INDEX = 1