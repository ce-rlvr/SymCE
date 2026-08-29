import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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

def conditions(witness):
    try:
        N, H, phi, M = witness
    except Exception:
        return [False, False, False]
        
    def is_group_perms(elems):
        if not elems: return False
        s = set(elems)
        for a in elems:
            try:
                inv = a**-1
            except Exception:
                try:
                    inv = ~a
                except Exception:
                    return False
            if inv not in s: return False
            for b in elems:
                try:
                    if a * b not in s: return False
                except Exception:
                    return False
        return True

    try:
        if hasattr(N, 'elements'):
            N_elems = list(N.elements)
        else:
            N_elems = list(N)
            
        if hasattr(H, 'elements'):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
            
        M_elems = list(M)
        
        if callable(phi):
            phi_dict = {}
            for h in H_elems:
                phi_dict[h] = {n: phi(h, n) for n in N_elems}
            phi = phi_dict
        elif isinstance(phi, dict):
            first_val = next(iter(phi.values())) if phi else None
            if callable(first_val):
                phi_dict = {}
                for h in H_elems:
                    if h in phi:
                        phi_dict[h] = {n: phi[h](n) for n in N_elems}
                phi = phi_dict

        h1_ok = False
        if is_group_perms(N_elems) and is_group_perms(H_elems) and is_group_perms(M_elems):
            if set(M_elems).issubset(set(N_elems)):
                phi_ok = True
                for h in H_elems:
                    if h not in phi:
                        phi_ok = False; break
                    phi_h = phi[h]
                    if set(phi_h.keys()) != set(N_elems) or set(phi_h.values()) != set(N_elems):
                        phi_ok = False; break
                    for n1 in N_elems:
                        for n2 in N_elems:
                            if phi_h[n1 * n2] != phi_h[n1] * phi_h[n2]:
                                phi_ok = False; break
                    if not phi_ok: break
                
                if phi_ok:
                    for h1 in H_elems:
                        for h2 in H_elems:
                            h12 = h1 * h2
                            for n in N_elems:
                                if phi[h12][n] != phi[h1][phi[h2][n]]:
                                    phi_ok = False; break
                            if not phi_ok: break
                h1_ok = phi_ok
    except Exception:
        h1_ok = False

    try:
        h2_ok = True
        M_set = set(M_elems)
        for h in H_elems:
            mapped_M = set(phi[h][m] for m in M_elems)
            if mapped_M != M_set:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    try:
        M_set = set(M_elems)
        neg_q = False
        for n in N_elems:
            try:
                n_inv = n**-1
            except Exception:
                n_inv = ~n
            for m in M_elems:
                if n * m * n_inv not in M_set:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G = N \\rtimes_\\phi H is the external semidirect product of groups N and H via \\phi",
    "H_2: For all h \\in H, \\phi_h(M) = M",
    "¬Q: M \\times \\{1_H\\} is not a normal subgroup of G, or the quotient is not isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2