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

def conditions(witness):
    try:
        G, H, X, action = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    try:
        h2 = True
        X_list = list(X)
        if len(X_list) == 0:
            h2 = False
        else:
            G_elements = list(G.elements)
            for g in G_elements:
                for x in X_list:
                    res = action(g, x)
                    found = False
                    for item in X_list:
                        if bool(res == item):
                            found = True
                            break
                    if not found:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    try:
        X_list = list(X)
        H_elements = list(H.elements)
        X_H = []
        for x in X_list:
            is_fixed = True
            for h in H_elements:
                if not bool(action(h, x) == x):
                    is_fixed = False
                    break
            if is_fixed:
                X_H.append(x)
                
        G_elements = list(G.elements)
        H_set = set(H_elements)
        N_G_H = []
        for g in G_elements:
            g_inv = ~g
            is_in_normalizer = True
            for h in H_elements:
                if (g * h * g_inv) not in H_set:
                    is_in_normalizer = False
                    break
            if is_in_normalizer:
                N_G_H.append(g)
                
        neg_q = False
        for g in N_G_H:
            for x in X_H:
                res = action(g, x)
                found = False
                for item in X_H:
                    if bool(res == item):
                        found = True
                        break
                if not found:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The operation * maps G x X to X",
    "¬Q: There exists g in N_G(H) and x in X^H such that g * x is not in X^H"
]

N_HYP = 2
NEG_Q_INDEX = 2