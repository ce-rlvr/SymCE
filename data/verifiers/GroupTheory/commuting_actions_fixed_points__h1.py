import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
    "H_1: H is a group acting on the set X",
    "H_2: The actions of G and H commute",
    "¬Q: The set of fixed points X^H is not invariant under the action of G (e.g., G does not act on X)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def apply_op(f, x):
    """Helper to apply a transformation (dict, function, or SymPy Permutation) to an element."""
    if isinstance(f, dict):
        return f[x]
    else:
        return f(x)

def conditions(witness):
    try:
        X = witness['X']
        H = witness['H']
        G = witness['G']
    except Exception:
        return [False, False, False]
        
    # H_1: H is a group acting on X
    try:
        h1_ok = True
        if not H:
            h1_ok = False
        else:
            # 1. Check for identity
            has_id = False
            for h in H:
                if all(apply_op(h, x) == x for x in X):
                    has_id = True
                    break
            if not has_id:
                h1_ok = False
                
            # 2. Check closure under composition
            if h1_ok:
                for h1 in H:
                    for h2 in H:
                        comp_found = False
                        for h3 in H:
                            if all(apply_op(h1, apply_op(h2, x)) == apply_op(h3, x) for x in X):
                                comp_found = True
                                break
                        if not comp_found:
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
                        
            # 3. Check for inverses
            if h1_ok:
                for h in H:
                    inv_found = False
                    for h_inv in H:
                        if all(apply_op(h, apply_op(h_inv, x)) == x and apply_op(h_inv, apply_op(h, x)) == x for x in X):
                            inv_found = True
                            break
                    if not inv_found:
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    # H_2: actions of G and H commute
    try:
        h2_ok = True
        for g in G:
            for h in H:
                for x in X:
                    if apply_op(g, apply_op(h, x)) != apply_op(h, apply_op(g, x)):
                        h2_ok = False
                        break
                if not h2_ok:
                    break
            if not h2_ok:
                break
    except Exception:
        h2_ok = False

    # Q: X^H is invariant under the action of G
    # For this to be true, G must actually be a group acting on X, and X^H must be invariant.
    try:
        g_is_group = True
        if not G:
            g_is_group = False
        else:
            try:
                # 1. Check for identity
                has_id = False
                for g in G:
                    if all(apply_op(g, x) == x for x in X):
                        has_id = True
                        break
                if not has_id:
                    g_is_group = False
                    
                # 2. Check closure under composition
                if g_is_group:
                    for g1 in G:
                        for g2 in G:
                            comp_found = False
                            for g3 in G:
                                if all(apply_op(g1, apply_op(g2, x)) == apply_op(g3, x) for x in X):
                                    comp_found = True
                                    break
                            if not comp_found:
                                g_is_group = False
                                break
                        if not g_is_group:
                            break
                            
                # 3. Check for inverses
                if g_is_group:
                    for g in G:
                        inv_found = False
                        for g_inv in G:
                            if all(apply_op(g, apply_op(g_inv, x)) == x and apply_op(g_inv, apply_op(g, x)) == x for x in X):
                                inv_found = True
                                break
                        if not inv_found:
                            g_is_group = False
                            break
            except Exception:
                # If applying g raises an exception, it's not a valid action on X
                g_is_group = False
                        
        try:
            # Find fixed points X^H
            X_H = []
            for x in X:
                if all(apply_op(h, x) == x for h in H):
                    X_H.append(x)
                    
            # Check invariance
            invariant = True
            for g in G:
                for x in X_H:
                    if apply_op(g, x) not in X_H:
                        invariant = False
                        break
                if not invariant:
                    break
        except Exception:
            invariant = False
                
        Q = g_is_group and invariant
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1_ok, h2_ok, neg_Q]