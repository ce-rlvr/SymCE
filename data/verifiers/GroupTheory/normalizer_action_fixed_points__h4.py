import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_attr(w, name):
    if isinstance(w, dict):
        return w.get(name)
    return getattr(w, name, None)

def conditions(witness) -> list[bool]:
    G = get_attr(witness, 'G')
    op = get_attr(witness, 'op')
    inv = get_attr(witness, 'inv')
    identity = get_attr(witness, 'id')
    X = get_attr(witness, 'X')
    action = get_attr(witness, 'action')
    H = get_attr(witness, 'H')
    X_H = get_attr(witness, 'X_H')

    # H_1: G is a group acting on a set X
    try:
        h1_ok = False
        if G is not None and op is not None and inv is not None and identity is not None and X is not None and action is not None:
            is_group = True
            if identity not in G:
                is_group = False
            else:
                for g in G:
                    if op(identity, g) != g or op(g, identity) != g:
                        is_group = False
                        break
                    if op(g, inv(g)) != identity or op(inv(g), g) != identity:
                        is_group = False
                        break
                if is_group:
                    for g1 in G:
                        for g2 in G:
                            g12 = op(g1, g2)
                            if g12 not in G:
                                is_group = False
                                break
                            for g3 in G:
                                if op(g1, op(g2, g3)) != op(g12, g3):
                                    is_group = False
                                    break
                            if not is_group:
                                break
                        if not is_group:
                            break
            
            is_action = True
            if is_group:
                for x in X:
                    if action(identity, x) != x:
                        is_action = False
                        break
                    for g in G:
                        if action(g, x) not in X:
                            is_action = False
                            break
                    if not is_action:
                        break
                
                if is_action:
                    for x in X:
                        for g1 in G:
                            for g2 in G:
                                g12 = op(g1, g2)
                                if action(g1, action(g2, x)) != action(g12, x):
                                    is_action = False
                                    break
                            if not is_action:
                                break
                        if not is_action:
                            break
            h1_ok = is_group and is_action
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = False
        if h1_ok and H is not None:
            is_subgroup = True
            if identity not in H:
                is_subgroup = False
            else:
                for h in H:
                    if h not in G:
                        is_subgroup = False
                        break
                    if inv(h) not in H:
                        is_subgroup = False
                        break
                    for h2 in H:
                        if op(h, h2) not in H:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            h2_ok = is_subgroup
    except Exception:
        h2_ok = False

    # H_3: X^H is the set of elements in X fixed by all elements of H
    try:
        h3_ok = False
        if h1_ok and h2_ok and X_H is not None:
            expected_X_H = []
            for x in X:
                fixed = True
                for h in H:
                    if action(h, x) != x:
                        fixed = False
                        break
                if fixed:
                    expected_X_H.append(x)
            
            all_in = True
            for x in X_H:
                if x not in expected_X_H:
                    all_in = False
                    break
            if all_in:
                for x in expected_X_H:
                    if x not in X_H:
                        all_in = False
                        break
            h3_ok = all_in
    except Exception:
        h3_ok = False

    # ¬Q: For any n \in N_G(H) and x \in X^H, the element n \cdot x is in X^H.
    # Negation: There exists n \in N_G(H) and x \in X^H such that n \cdot x \notin X^H.
    try:
        neg_q = False
        if h1_ok and h2_ok and h3_ok:
            N_G_H = []
            for g in G:
                normalizes = True
                for h in H:
                    ghg_inv = op(g, op(h, inv(g)))
                    if ghg_inv not in H:
                        normalizes = False
                        break
                    g_inv_hg = op(inv(g), op(h, g))
                    if g_inv_hg not in H:
                        normalizes = False
                        break
                if normalizes:
                    N_G_H.append(g)
            
            for n in N_G_H:
                for x in X_H:
                    nx = action(n, x)
                    if nx not in X_H:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: X^H is the set of elements in X fixed by all elements of H",
    "¬Q: There exists n in N_G(H) and x in X^H such that n \cdot x is not in X^H"
]

N_HYP = 3
NEG_Q_INDEX = 3