import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, N, X, raw_action = witness
            if callable(raw_action):
                action = raw_action
            elif isinstance(raw_action, dict):
                action = lambda g, x: raw_action[(g, x)]
            else:
                return [False, False, False]
        elif len(witness) == 2:
            G, N = witness
            X = list(G.domain)
            action = lambda g, x: g(x)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        if not isinstance(G, PermutationGroup):
            h1 = False
        if not isinstance(X, (list, set, tuple)):
            h1 = False
        
        if h1:
            X_list = list(X)
            X_set = set(X_list)
            elems = list(G.elements)
            id_g = G.identity
            
            for x in X_list:
                if action(id_g, x) != x:
                    h1 = False
                    break
                    
            if h1:
                for g in elems:
                    for x in X_list:
                        if action(g, x) not in X_set:
                            h1 = False
                            break
                    if not h1: break
                    
            if h1:
                for g in elems:
                    for h in elems:
                        for x in X_list:
                            if action(g, action(h, x)) != action(g*h, x):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
    except Exception:
        h1 = False

    try:
        h2 = True
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            N_elems = list(N.elements)
            G_elems = list(G.elements)
            N_set = set(N_elems)
            
            for n in N_elems:
                if n not in G_elems:
                    h2 = False
                    break
                    
            if h2:
                for g in G_elems:
                    g_inv = g**-1
                    for n in N_elems:
                        if (g * n * g_inv) not in N_set:
                            h2 = False
                            break
                    if not h2: break
    except Exception:
        h2 = False

    try:
        N_elems = list(N.elements)
        G_elems = list(G.elements)
        X_list = list(X)
        
        X_N = []
        for x in X_list:
            is_fixed = True
            for n in N_elems:
                if action(n, x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                X_N.append(x)
                
        neg_q = False
        X_N_set = set(X_N)
        for g in G_elems:
            for x in X_N:
                if action(g, x) not in X_N_set:
                    neg_q = True
                    break
            if neg_q: break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 2
NEG_Q_INDEX = 2