import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        X = witness['X']
        Y = witness['Y']
        act_X_raw = witness['action_X']
        act_Y_raw = witness['action_Y']
        x = witness['x']
        y = witness['y']
        
        if hasattr(G, 'elements'):
            G_elems = list(G.elements)
            mul = lambda g1, g2: g1 * g2
        else:
            G_elems = list(G)
            mul = witness.get('mul', lambda g1, g2: g1 * g2)
            
        def act_X(g, a):
            if callable(act_X_raw): return act_X_raw(g, a)
            return act_X_raw[(g, a)]
            
        def act_Y(g, a):
            if callable(act_Y_raw): return act_Y_raw(g, a)
            return act_Y_raw[(g, a)]
            
        identities = []
        for cand in G_elems:
            if all(mul(cand, g) == g and mul(g, cand) == g for g in G_elems):
                identities.append(cand)
        e = identities[0] if identities else None
        
        inv = {}
        if e is not None:
            for g in G_elems:
                for h in G_elems:
                    if mul(g, h) == e and mul(h, g) == e:
                        inv[g] = h
                        break
                        
        X_set = set(X)
        Y_set = set(Y)
        
        def is_transitive(S_set, act):
            if not S_set: return False
            for g in G_elems:
                for a in S_set:
                    if act(g, a) not in S_set: return False
            if e is not None:
                for a in S_set:
                    if act(e, a) != a: return False
            for g1 in G_elems:
                for g2 in G_elems:
                    g12 = mul(g1, g2)
                    for a in S_set:
                        if act(g1, act(g2, a)) != act(g12, a): return False
            for a in S_set:
                orbit = {act(g, a) for g in G_elems}
                if orbit != S_set: return False
            return True
            
        H1 = is_transitive(X_set, act_X) and is_transitive(Y_set, act_Y)
    except Exception:
        H1 = False

    try:
        H2 = (x in X_set) and (y in Y_set)
    except Exception:
        H2 = False

    try:
        isomorphic = False
        for z in Y_set:
            f = {}
            well_defined = True
            for g in G_elems:
                a = act_X(g, x)
                b = act_Y(g, z)
                if a in f:
                    if f[a] != b:
                        well_defined = False
                        break
                else:
                    f[a] = b
            if not well_defined: continue
            if len(f) != len(X_set): continue
            if set(f.values()) != Y_set: continue
            if len(set(f.values())) != len(f): continue
            
            is_g_map = True
            for h in G_elems:
                for a in X_set:
                    if f[act_X(h, a)] != act_Y(h, f[a]):
                        is_g_map = False
                        break
                if not is_g_map: break
            if is_g_map:
                isomorphic = True
                break
                
        Stab_x = {g for g in G_elems if act_X(g, x) == x}
        Stab_y = {g for g in G_elems if act_Y(g, y) == y}
        
        condition_holds = False
        for g in G_elems:
            if g not in inv: continue
            g_inv = inv[g]
            conj = {mul(mul(g, h), g_inv) for h in Stab_x}
            if conj == Stab_y:
                condition_holds = True
                break
                
        Q = (isomorphic == condition_holds)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: X and Y are transitive G-sets",
    "H_2: x in X and y in Y",
    "¬Q: It is not the case that (X and Y are isomorphic as G-sets iff there exists g in G such that g Stab_G(x) g^-1 = Stab_G(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2