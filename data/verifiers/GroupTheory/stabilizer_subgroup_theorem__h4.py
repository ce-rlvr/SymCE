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
        G, X, action, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = False
        if hasattr(G, 'elements') and hasattr(G, 'identity'):
            elements = list(G.elements)
            e = G.identity
            h1 = True
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = False
        if hasattr(X, '__iter__'):
            X_list = list(X)
            h2 = True
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = False
        if h1 and h2:
            is_valid = True
            for y in X_list:
                if action(e, y) != y:
                    is_valid = False
                    break
            
            if is_valid:
                is_left = True
                is_right = True
                for g in elements:
                    for h in elements:
                        for y in X_list:
                            res_h = action(h, y)
                            if res_h not in X_list:
                                is_valid = False
                                break
                            res_g_h = action(g, res_h)
                            if res_g_h not in X_list:
                                is_valid = False
                                break
                            
                            res_gh = action(g * h, y)
                            res_hg = action(h * g, y)
                            
                            if res_g_h != res_gh:
                                is_left = False
                            if res_g_h != res_hg:
                                is_right = False
                        if not is_valid:
                            break
                    if not is_valid:
                        break
                if is_valid and (is_left or is_right):
                    h3 = True
    except Exception:
        h3 = False

    # neg_Q: Stab(x) is NOT a subgroup of G
    try:
        neg_q = False
        if h1:
            stab_x = set()
            for g in elements:
                if action(g, x) == x:
                    stab_x.add(g)
            
            is_sub = True
            if e not in stab_x:
                is_sub = False
            else:
                for g in stab_x:
                    if g**-1 not in stab_x:
                        is_sub = False
                        break
                    for h in stab_x:
                        if g * h not in stab_x:
                            is_sub = False
                            break
                    if not is_sub:
                        break
            neg_q = not is_sub
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "¬Q: Stab(x) is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3