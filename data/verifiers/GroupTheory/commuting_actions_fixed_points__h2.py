import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = list(witness['G'])
            H = list(witness['H'])
            X = list(witness['X'])
            action_G = witness['action_G']
            action_H = witness['action_H']
            mul_G = witness.get('mul_G', lambda g1, g2: g1 * g2)
        else:
            G = list(witness.G)
            H = list(witness.H)
            X = list(witness.X)
            action_G = witness.action_G
            action_H = witness.action_H
            mul_G = getattr(witness, 'mul_G', lambda g1, g2: g1 * g2)
    except Exception:
        return [False, False, False]

    # H1: G is a group acting on a set X
    try:
        is_group = False
        identity = None
        for e in G:
            if all(mul_G(e, g) == g and mul_G(g, e) == g for g in G):
                identity = e
                break
        
        if identity is not None:
            closure = True
            assoc = True
            inverses = True
            for g1 in G:
                has_inv = False
                for g2 in G:
                    try:
                        m = mul_G(g1, g2)
                    except Exception:
                        closure = False
                        continue
                    if not contains(G, m):
                        closure = False
                    if m == identity and mul_G(g2, g1) == identity:
                        has_inv = True
                    for g3 in G:
                        if mul_G(g1, mul_G(g2, g3)) != mul_G(mul_G(g1, g2), g3):
                            assoc = False
                if not has_inv:
                    inverses = False
            if closure and assoc and inverses:
                is_group = True

        acts_on_X = True
        if is_group:
            for x in X:
                if action_G(identity, x) != x:
                    acts_on_X = False
                for g in G:
                    gx = action_G(g, x)
                    if not contains(X, gx):
                        acts_on_X = False
                    for g2 in G:
                        if action_G(g, action_G(g2, x)) != action_G(mul_G(g, g2), x):
                            acts_on_X = False
        else:
            acts_on_X = False
            
        H1_ok = is_group and acts_on_X
    except Exception:
        H1_ok = False

    # H2: The actions of G and H commute
    try:
        H2_ok = True
        for h in H:
            for x in X:
                hx = action_H(h, x)
                if not contains(X, hx):
                    H2_ok = False
                for g in G:
                    if action_G(g, hx) != action_H(h, action_G(g, x)):
                        H2_ok = False
    except Exception:
        H2_ok = False

    # neg_Q: The set of fixed points X^H is not invariant under the action of G
    try:
        X_H = []
        for x in X:
            is_fixed = True
            for h in H:
                if action_H(h, x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                X_H.append(x)
        
        Q_ok = True
        for x in X_H:
            for g in G:
                gx = action_G(g, x)
                if not contains(X_H, gx):
                    Q_ok = False
                    break
        neg_Q_ok = not Q_ok
    except Exception:
        neg_Q_ok = False

    return [H1_ok, H2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The actions of G and H commute",
    "¬Q: The set of fixed points X^H is not invariant under the action of G"
]

N_HYP = 2
NEG_Q_INDEX = 2