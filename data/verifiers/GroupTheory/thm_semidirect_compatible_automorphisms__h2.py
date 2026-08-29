import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def get_identity(G, elems):
    if hasattr(G, 'identity'):
        return G.identity
    for e in elems:
        if all(e * x == x and x * e == x for x in elems):
            return e
    return None

def conditions(witness):
    try:
        N = witness['N']
        H = witness['H']
        
        N_elems = get_elements(N)
        H_elems = get_elements(H)
        
        id_H = get_identity(H, H_elems)
        if id_H is None:
            return [False, False, False]
            
        set_N = set(N_elems)
        set_H = set(H_elems)
        
        phi_raw = witness['phi']
        alpha_raw = witness['alpha']
        beta_raw = witness['beta']
        
        if callable(alpha_raw):
            alpha = {n: alpha_raw(n) for n in N_elems}
        else:
            alpha = alpha_raw
            
        if callable(beta_raw):
            beta = {h: beta_raw(h) for h in H_elems}
        else:
            beta = beta_raw
            
        phi = {}
        for h in H_elems:
            phi_h_raw = phi_raw(h) if callable(phi_raw) else phi_raw[h]
            if callable(phi_h_raw):
                phi[h] = {n: phi_h_raw(n) for n in N_elems}
            else:
                phi[h] = phi_h_raw
                
    except Exception:
        return [False, False, False]
        
    # H1: G = N \rtimes_\phi H is an external semidirect product
    try:
        h1_ok = True
        for h in H_elems:
            if h not in phi:
                h1_ok = False
                break
            phi_h = phi[h]
            if set(phi_h.keys()) != set_N or set(phi_h.values()) != set_N:
                h1_ok = False
                break
            for n1 in N_elems:
                for n2 in N_elems:
                    if phi_h[n1 * n2] != phi_h[n1] * phi_h[n2]:
                        h1_ok = False
                        break
                if not h1_ok: break
            if not h1_ok: break
            
        if h1_ok:
            for h1 in H_elems:
                for h2 in H_elems:
                    phi_h1h2 = phi[h1 * h2]
                    phi_h1 = phi[h1]
                    phi_h2 = phi[h2]
                    for n in N_elems:
                        if phi_h1h2[n] != phi_h1[phi_h2[n]]:
                            h1_ok = False
                            break
                    if not h1_ok: break
                if not h1_ok: break
                
        if h1_ok:
            for n in N_elems:
                if phi[id_H][n] != n:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H2: compatibility condition
    try:
        h2_ok = True
        if set(alpha.keys()) != set_N or set(alpha.values()) != set_N:
            h2_ok = False
        if set(beta.keys()) != set_H or set(beta.values()) != set_H:
            h2_ok = False
            
        if h2_ok:
            for h in H_elems:
                for n in N_elems:
                    if alpha[phi[h][n]] != phi[beta[h]][alpha[n]]:
                        h2_ok = False
                        break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    # neg_Q: gamma is NOT a group automorphism
    try:
        is_hom = True
        for n1 in N_elems:
            for h1 in H_elems:
                for n2 in N_elems:
                    for h2 in H_elems:
                        lhs_n = alpha[n1 * phi[h1][n2]]
                        lhs_h = beta[h1 * h2]
                        
                        rhs_n = alpha[n1] * phi[beta[h1]][alpha[n2]]
                        rhs_h = beta[h1] * beta[h2]
                        
                        if lhs_n != rhs_n or lhs_h != rhs_h:
                            is_hom = False
                            break
                    if not is_hom: break
                if not is_hom: break
            if not is_hom: break
            
        neg_q = not is_hom
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G = N \\rtimes_\\phi H is an external semidirect product with action \\phi: H \\to Aut(N)",
    "H_2: For all h \\in H, \\alpha \\circ \\phi(h) \\circ \\alpha^{-1} = \\phi(\\beta(h))",
    "¬Q: The bijective map \\gamma(n, h) = (\\alpha(n), \\beta(h)) is NOT a group automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2