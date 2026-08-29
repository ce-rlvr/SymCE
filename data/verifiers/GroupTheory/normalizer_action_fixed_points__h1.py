import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_elements(group):
    if hasattr(group, 'generate_dimino'):
        return list(group.generate_dimino())
    elif hasattr(group, 'elements'):
        return list(group.elements)
    else:
        return list(group)

def same_elements(it1, it2):
    l1 = list(it1)
    l2 = list(it2)
    for x in l1:
        if x not in l2: return False
    for x in l2:
        if x not in l1: return False
    return True

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness should be a tuple: (G, H, X, action) 
    Optionally: (G, H, X, action, X_H) or (G, H, X, action, X_H, N_G_H)
    """
    try:
        if len(witness) == 4:
            G, H, X, action = witness
            X_H_provided = None
            N_G_H_provided = None
        elif len(witness) == 5:
            G, H, X, action, X_H_provided = witness
            N_G_H_provided = None
        elif len(witness) == 6:
            G, H, X, action, X_H_provided, N_G_H_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1_ok = bool(H.is_subgroup(G))
        else:
            G_elems = get_elements(G)
            H_elems = get_elements(H)
            h1_ok = all(h in G_elems for h in H_elems)
            # Check closure for fallback
            if h1_ok:
                for h1 in H_elems:
                    for h2 in H_elems:
                        if (h1 * h2) not in H_elems:
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
    except Exception:
        h1_ok = False

    def act(g, x):
        if callable(action):
            return action(g, x)
        return action[(g, x)]

    # H_2: X^H is the set of elements in X fixed by all elements of H
    try:
        H_elems = get_elements(H)
        expected_X_H = []
        for x in X:
            fixed = True
            for h in H_elems:
                try:
                    if act(h, x) != x:
                        fixed = False
                        break
                except Exception:
                    fixed = False
                    break
            if fixed:
                expected_X_H.append(x)
        
        if X_H_provided is not None:
            try:
                h2_ok = same_elements(X_H_provided, expected_X_H)
            except Exception:
                h2_ok = False
            X_H = X_H_provided
        else:
            h2_ok = True
            X_H = expected_X_H
    except Exception:
        h2_ok = False
        X_H = []

    # H_3: N_G(H) is the normalizer of H in G
    try:
        G_elems = get_elements(G)
        H_elems = get_elements(H)
        H_list = list(H_elems)
        expected_N_G_H = []
        for g in G_elems:
            is_norm = True
            for h in H_list:
                try:
                    conj = g * h * (g**-1)
                except Exception:
                    try:
                        conj = g * h * (~g)
                    except Exception:
                        conj = g * h * g.inv()
                if conj not in H_list:
                    is_norm = False
                    break
            if is_norm:
                expected_N_G_H.append(g)
                
        if N_G_H_provided is not None:
            try:
                h3_ok = same_elements(N_G_H_provided, expected_N_G_H)
            except Exception:
                h3_ok = False
            N_G_H = N_G_H_provided
        else:
            h3_ok = True
            N_G_H = expected_N_G_H
    except Exception:
        h3_ok = False
        N_G_H = []

    # neg_Q: For any n \in N_G(H) and x \in X^H, the element n \cdot x is in X^H.
    # Negation: There exists n \in N_G(H) and x \in X^H such that n \cdot x \notin X^H.
    try:
        neg_q = False
        for n in N_G_H:
            for x in X_H:
                try:
                    nx = act(n, x)
                    if nx not in X_H:
                        neg_q = True
                        break
                except Exception:
                    # If action is undefined, it's not in X^H
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: X^H is the set of elements in X fixed by all elements of H",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: There exists n in N_G(H) and x in X^H such that n \cdot x is not in X^H"
]

N_HYP = 3
NEG_Q_INDEX = 3