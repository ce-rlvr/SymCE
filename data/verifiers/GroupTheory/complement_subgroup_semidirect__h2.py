import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
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
    "H_1: N and H are groups",
    "H_2: G is the external semidirect product of N and H via phi",
    "¬Q: H' is not a subgroup isomorphic to H, or G is not the internal semidirect product of N' and H'"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]
        
    try:
        N_elems = list(N.elements) if hasattr(N, 'elements') else list(N)
        H_elems = list(H.elements) if hasattr(H, 'elements') else list(H)
    except Exception:
        return [False, False, False]

    def find_identity(elems):
        for e in elems:
            is_id = True
            for x in elems:
                try:
                    if e * x != x or x * e != x:
                        is_id = False
                        break
                except Exception:
                    is_id = False
                    break
            if is_id:
                return e
        return None

    def is_group(elems):
        if not elems: return False, None
        e = find_identity(elems)
        if e is None: return False, None
        for x in elems:
            has_inv = False
            for y in elems:
                try:
                    if x * y == e and y * x == e:
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv: return False, None
            for y in elems:
                try:
                    if (x * y) not in elems:
                        return False, None
                except Exception:
                    return False, None
        return True, e

    try:
        N_is_group, e_N = is_group(N_elems)
        H_is_group, e_H = is_group(H_elems)
        h1_ok = N_is_group and H_is_group
    except Exception:
        h1_ok = False

    def apply_phi(h, n):
        if isinstance(phi, dict):
            phi_h = phi[h]
        else:
            phi_h = phi(h)
        if isinstance(phi_h, dict):
            return phi_h[n]
        else:
            return phi_h(n)

    try:
        h2_ok = True
        for h in H_elems:
            for n in N_elems:
                res = apply_phi(h, n)
                if res not in N_elems:
                    h2_ok = False
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    try:
        if e_N is None or e_H is None:
            neg_q = False
        else:
            def G_mul(g1, g2):
                return (g1[0] * apply_phi(g1[1], g2[0]), g1[1] * g2[1])
                
            G_elems = [(n, h) for n in N_elems for h in H_elems]
            
            conclusion_holds = True
            
            is_assoc = True
            for g1 in G_elems:
                for g2 in G_elems:
                    for g3 in G_elems:
                        if G_mul(G_mul(g1, g2), g3) != G_mul(g1, G_mul(g2, g3)):
                            is_assoc = False
                            break
                    if not is_assoc: break
                if not is_assoc: break
                
            if not is_assoc:
                conclusion_holds = False
            else:
                e_G = (e_N, e_H)
                is_id = True
                for g in G_elems:
                    if G_mul(e_G, g) != g or G_mul(g, e_G) != g:
                        is_id = False
                        break
                if not is_id:
                    conclusion_holds = False
                else:
                    has_invs = True
                    for g in G_elems:
                        has_inv = False
                        for inv in G_elems:
                            if G_mul(g, inv) == e_G and G_mul(inv, g) == e_G:
                                has_inv = True
                                break
                        if not has_inv:
                            has_invs = False
                            break
                    if not has_invs:
                        conclusion_holds = False
                        
            if conclusion_holds:
                for h1 in H_elems:
                    for h2 in H_elems:
                        if G_mul((e_N, h1), (e_N, h2)) != (e_N, h1 * h2):
                            conclusion_holds = False
                            break
                    if not conclusion_holds: break
                    
            if conclusion_holds:
                for n1 in N_elems:
                    for n2 in N_elems:
                        if G_mul((n1, e_H), (n2, e_H)) != (n1 * n2, e_H):
                            conclusion_holds = False
                            break
                    if not conclusion_holds: break
                    
            if conclusion_holds:
                for g in G_elems:
                    g_inv = None
                    for inv in G_elems:
                        if G_mul(g, inv) == e_G and G_mul(inv, g) == e_G:
                            g_inv = inv
                            break
                    for n in N_elems:
                        conj = G_mul(G_mul(g, (n, e_H)), g_inv)
                        if conj[1] != e_H:
                            conclusion_holds = False
                            break
                    if not conclusion_holds: break
                    
            neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]