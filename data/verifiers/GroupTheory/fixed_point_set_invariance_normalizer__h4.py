import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def check_sets_equal(set1, set2):
    for item1 in set1:
        if not any(eq(item1, item2) for item2 in set2):
            return False
    for item2 in set2:
        if not any(eq(item1, item2) for item1 in set1):
            return False
    return True

def check_group_and_action(G, X, action):
    identities = []
    for e in G:
        try:
            if all(eq(e * g, g) for g in G) and all(eq(g * e, g) for g in G):
                identities.append(e)
        except Exception:
            pass
    if not identities:
        return False
    e = identities[0]
    
    for g in G:
        has_inv = False
        for g_inv in G:
            if eq(g * g_inv, e) and eq(g_inv * g, e):
                has_inv = True
                break
        if not has_inv:
            return False

    for x in X:
        if not eq(action(e, x), x):
            return False
            
    is_left = True
    is_right = True
    for g1 in G:
        for g2 in G:
            try:
                g1g2 = g1 * g2
            except Exception:
                return False
            
            if not any(eq(g1g2, g) for g in G):
                return False
                
            for x in X:
                try:
                    res1 = action(g1, action(g2, x))
                    res_left = action(g1g2, x)
                    res_right = action(g2 * g1, x)
                    if not eq(res1, res_left):
                        is_left = False
                    if not eq(res1, res_right):
                        is_right = False
                except Exception:
                    return False
                    
    return is_left or is_right

def check_subgroup(G_list, H_list):
    if not H_list:
        return False
    for h in H_list:
        if not any(eq(h, g) for g in G_list):
            return False
    for h1 in H_list:
        for h2 in H_list:
            try:
                h1h2 = h1 * h2
            except Exception:
                return False
            if not any(eq(h1h2, h) for h in H_list):
                return False
    identities = []
    for e in H_list:
        if all(eq(e * h, h) for h in H_list):
            identities.append(e)
    if not identities:
        return False
    e = identities[0]
    for h in H_list:
        has_inv = False
        for h_inv in H_list:
            if eq(h * h_inv, e) and eq(h_inv * h, e):
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get("G", [])
            X = witness.get("X", [])
            action = witness.get("action", None)
            H = witness.get("H", [])
            X_H = witness.get("X_H", None)
        else:
            if len(witness) == 4:
                G, X, action, H = witness
                X_H = None
            elif len(witness) == 5:
                G, X, action, H, X_H = witness
            else:
                return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(G, 'elements'):
            G_list = list(G.elements)
        elif hasattr(G, 'generate'):
            G_list = list(G.generate())
        else:
            G_list = list(G)
    except Exception:
        G_list = []

    try:
        if hasattr(H, 'elements'):
            H_list = list(H.elements)
        elif hasattr(H, 'generate'):
            H_list = list(H.generate())
        else:
            H_list = list(H)
    except Exception:
        H_list = []

    try:
        X_list = list(X)
    except Exception:
        X_list = []

    # H1: G is a group acting on a set X
    try:
        h1_ok = check_group_and_action(G_list, X_list, action)
    except Exception:
        h1_ok = False

    # H2: H is a subgroup of G
    try:
        h2_ok = check_subgroup(G_list, H_list)
    except Exception:
        h2_ok = False

    # H3: X^H is the set of fixed points of H
    try:
        computed_X_H = []
        for x in X_list:
            if all(eq(action(h, x), x) for h in H_list):
                computed_X_H.append(x)
        
        if X_H is not None:
            h3_ok = check_sets_equal(X_H, computed_X_H)
        else:
            X_H = computed_X_H
            h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: There exists g in N_G(H) and x in X^H such that g * x is not in X^H
    try:
        N_G_H = []
        for g in G_list:
            gH = [g * h for h in H_list]
            Hg = [h * g for h in H_list]
            if check_sets_equal(gH, Hg):
                N_G_H.append(g)
                
        neg_q = False
        for g in N_G_H:
            for x in X_H:
                gx = action(g, x)
                if not any(eq(gx, x_h) for x_h in X_H):
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: X^H is the set of fixed points of H",
    "¬Q: There exists g in N_G(H) and x in X^H such that g * x is not in X^H"
]

N_HYP = 3
NEG_Q_INDEX = 3