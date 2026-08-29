import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
    # Extract witness components
    is_default_op = False
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            action = witness['action']
            x = witness['x']
            if 'op' in witness:
                op = witness['op']
            else:
                op = lambda a, b: a * b
                is_default_op = True
        elif len(witness) == 5:
            G, op, X, action, x = witness
        elif len(witness) == 4:
            G, X, action, x = witness
            op = lambda a, b: a * b
            is_default_op = True
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # Get elements of G
    try:
        G_elems = list(G)
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    h1 = False
    try:
        unique_elems = []
        for e in G_elems:
            if e not in unique_elems:
                unique_elems.append(e)
        if len(unique_elems) != len(G_elems):
            h1 = False
        elif isinstance(G, PermutationGroup) and is_default_op:
            h1 = True
        else:
            if len(G_elems) > 0:
                identity = None
                for e in G_elems:
                    if all(op(e, a) == a and op(a, e) == a for a in G_elems):
                        identity = e
                        break
                if identity is not None:
                    is_group = True
                    for a in G_elems:
                        has_inv = False
                        for b in G_elems:
                            c = op(a, b)
                            if c not in G_elems:
                                is_group = False
                                break
                            if c == identity and op(b, a) == identity:
                                has_inv = True
                        if not is_group or not has_inv:
                            is_group = False
                            break
                    if is_group:
                        assoc = True
                        for a in G_elems:
                            for b in G_elems:
                                for c in G_elems:
                                    if op(op(a, b), c) != op(a, op(b, c)):
                                        assoc = False
                                        break
                                if not assoc: break
                            if not assoc: break
                        h1 = assoc
    except Exception:
        h1 = False

    # H_2: G acts on X
    h2 = False
    try:
        X_list = list(X)
        identity = None
        for e in G_elems:
            if all(op(e, a) == a and op(a, e) == a for a in G_elems):
                identity = e
                break
        
        if identity is not None:
            acts = True
            for y in X_list:
                if action(identity, y) != y:
                    acts = False
                    break
            if acts:
                for g in G_elems:
                    for h in G_elems:
                        gh = op(g, h)
                        for y in X_list:
                            if action(g, action(h, y)) != action(gh, y):
                                acts = False
                                break
                            if action(g, y) not in X_list:
                                acts = False
                                break
                        if not acts: break
                    if not acts: break
            h2 = acts
    except Exception:
        h2 = False

    # H_3: x is an element of X
    h3 = False
    try:
        X_list = list(X)
        h3 = x in X_list
    except Exception:
        h3 = False

    # ¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|
    neg_q = False
    try:
        orb = []
        stab = []
        for g in G_elems:
            y = action(g, x)
            if y not in orb:
                orb.append(y)
            if y == x:
                stab.append(g)
        neg_q = len(G_elems) != len(orb) * len(stab)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: |G| != |Orb_G(x)| * |Stab_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3