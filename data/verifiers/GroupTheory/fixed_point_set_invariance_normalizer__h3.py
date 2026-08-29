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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: There exists g in N_G(H) and x in X^H such that g * x is not in X^H"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    G = None
    H = None
    X = None
    action = None
    N = None
    
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            X = witness.get('X')
            action = witness.get('action')
            N = witness.get('N')
        elif isinstance(witness, tuple):
            if len(witness) >= 2: G = witness[0]; H = witness[1]
            if len(witness) >= 3: X = witness[2]
            if len(witness) >= 4: action = witness[3]
            if len(witness) >= 5: N = witness[4]
    except Exception:
        pass

    if G is None or H is None:
        return [False, False, False, False]

    try:
        if hasattr(G, 'elements'):
            G_elems = list(G.elements)
        elif isinstance(G, list):
            G_elems = G
        else:
            G_elems = list(G)
            
        if hasattr(H, 'elements'):
            H_elems = list(H.elements)
        elif isinstance(H, list):
            H_elems = H
        else:
            H_elems = list(H)
    except Exception:
        return [False, False, False, False]

    if X is None:
        try:
            if hasattr(G, 'domain'):
                X = list(G.domain)
            else:
                X = G_elems
        except Exception:
            return [False, False, False, False]

    if action is None:
        try:
            if hasattr(G, 'domain'):
                action = lambda g, x: g(x)
            else:
                action = lambda g, x: g * x
        except Exception:
            return [False, False, False, False]

    def eq(a, b):
        try:
            return bool(a == b)
        except Exception:
            return False

    # H1: G is a group acting on X
    h1 = False
    id_g = None
    try:
        for g in G_elems:
            is_id = True
            for a in G_elems:
                if not eq(g * a, a) or not eq(a * g, a):
                    is_id = False
                    break
            if is_id:
                id_g = g
                break
        
        if id_g is not None:
            acts_trivially = True
            for x in X:
                if not eq(action(id_g, x), x):
                    acts_trivially = False
                    break
            
            if acts_trivially:
                is_closed = True
                for g in G_elems:
                    for x in X:
                        res = action(g, x)
                        found = False
                        for y in X:
                            if eq(res, y):
                                found = True
                                break
                        if not found:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                
                if is_closed:
                    is_left = True
                    is_right = True
                    for g1 in G_elems:
                        for g2 in G_elems:
                            g12 = g1 * g2
                            g21 = g2 * g1
                            for x in X:
                                res = action(g1, action(g2, x))
                                if not eq(res, action(g12, x)):
                                    is_left = False
                                if not eq(res, action(g21, x)):
                                    is_right = False
                            if not is_left and not is_right:
                                break
                        if not is_left and not is_right:
                            break
                    h1 = is_left or is_right
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    h2 = False
    try:
        is_sub = True
        for h in H_elems:
            found = False
            for g in G_elems:
                if eq(h, g):
                    found = True
                    break
            if not found:
                is_sub = False
                break
                
        if is_sub and len(H_elems) > 0:
            for h1_elem in H_elems:
                for h2_elem in H_elems:
                    prod = h1_elem * h2_elem
                    found = False
                    for h in H_elems:
                        if eq(prod, h):
                            found = True
                            break
                    if not found:
                        is_sub = False
                        break
                if not is_sub:
                    break
            
            if is_sub:
                for h in H_elems:
                    inv_found = False
                    for h_inv in H_elems:
                        if eq(h * h_inv, id_g) and eq(h_inv * h, id_g):
                            inv_found = True
                            break
                    if not inv_found:
                        is_sub = False
                        break
        h2 = is_sub
    except Exception:
        h2 = False

    # H3: N is the normalizer of H in G
    h3 = False
    N_elems = []
    try:
        actual_N = []
        for g in G_elems:
            g_inv = None
            for a in G_elems:
                if eq(g * a, id_g) and eq(a * g, id_g):
                    g_inv = a
                    break
            if g_inv is not None:
                conj = []
                for h in H_elems:
                    conj.append(g * h * g_inv)
                
                is_eq = True
                for c in conj:
                    found = False
                    for h in H_elems:
                        if eq(c, h):
                            found = True
                            break
                    if not found:
                        is_eq = False
                        break
                if is_eq:
                    for h in H_elems:
                        found = False
                        for c in conj:
                            if eq(h, c):
                                found = True
                                break
                        if not found:
                            is_eq = False
                            break
                if is_eq:
                    actual_N.append(g)
        
        if N is None:
            N_elems = actual_N
            h3 = True
        else:
            if hasattr(N, 'elements'):
                N_elems = list(N.elements)
            elif isinstance(N, list):
                N_elems = N
            else:
                N_elems = list(N)
                
            is_eq = True
            for n in N_elems:
                found = False
                for an in actual_N:
                    if eq(n, an):
                        found = True
                        break
                if not found:
                    is_eq = False
                    break
            if is_eq:
                for an in actual_N:
                    found = False
                    for n in N_elems:
                        if eq(an, n):
                            found = True
                            break
                    if not found:
                        is_eq = False
                        break
            h3 = is_eq
    except Exception:
        h3 = False

    # neg_Q: exists g in N, x in X^H such that g * x not in X^H
    neg_q = False
    try:
        X_H = []
        for x in X:
            fixed = True
            for h in H_elems:
                if not eq(action(h, x), x):
                    fixed = False
                    break
            if fixed:
                X_H.append(x)
                
        for g in N_elems:
            for x in X_H:
                gx = action(g, x)
                in_X_H = False
                for xh in X_H:
                    if eq(gx, xh):
                        in_X_H = True
                        break
                if not in_X_H:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]