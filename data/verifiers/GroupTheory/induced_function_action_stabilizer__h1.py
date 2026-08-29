import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects to define in setup
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

def _get_inv(witness, g):
    if hasattr(witness, 'G_inv'): return witness.G_inv(g)
    if hasattr(witness, 'inv'): return witness.inv(g)
    try: return ~g
    except Exception: pass
    try: return g**-1
    except Exception: pass
    try: return -g
    except Exception: pass
    raise ValueError("No inverse provided or inferrable")

def _get_op(witness, g1, g2):
    if hasattr(witness, 'G_op'): return witness.G_op(g1, g2)
    if hasattr(witness, 'op'): return witness.op(g1, g2)
    try: return g1 * g2
    except Exception: pass
    try: return g1 + g2
    except Exception: pass
    raise ValueError("No group operation provided or inferrable")

def _get_action(witness, g, x):
    if hasattr(witness, 'action_X'): return witness.action_X(g, x)
    if hasattr(witness, 'action'): return witness.action(g, x)
    try: return g(x)
    except Exception: pass
    try: return g * x
    except Exception: pass
    raise ValueError("No action provided or inferrable")

def _get_f(witness, x):
    if hasattr(witness, 'f'):
        if callable(witness.f): return witness.f(x)
        return witness.f[x]
    raise ValueError("No function f provided")

def _get_id(witness, G):
    if hasattr(witness, 'G_id'): return witness.G_id
    if hasattr(witness, 'id'): return witness.id
    if hasattr(witness, 'identity'): return witness.identity
    for e in G:
        is_id = True
        for g in G:
            if _get_op(witness, e, g) != g or _get_op(witness, g, e) != g:
                is_id = False
                break
        if is_id:
            return e
    raise ValueError("No identity element found")

def conditions(witness):
    # H1: Y is a set
    try:
        Y = list(witness.Y)
        h1 = True
    except Exception:
        h1 = False

    # H2: Y^X is the set of all functions from X to Y
    try:
        X = list(witness.X)
        h2 = True
    except Exception:
        h2 = False

    # H3: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)
    # We verify that the operation is well-defined on X.
    try:
        h3 = True
        G = list(witness.G)
        for g in G:
            inv_g = _get_inv(witness, g)
            for x in X:
                act_x = _get_action(witness, inv_g, x)
                if act_x not in X:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    # H4: f is a function in Y^X
    try:
        h4 = True
        for x in X:
            fx = _get_f(witness, x)
            if fx not in Y:
                h4 = False
                break
    except Exception:
        h4 = False

    # neg_Q: The stabilizer of f in G is NOT the subgroup {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X}
    # This happens if the set S is not a valid subgroup.
    try:
        G = list(witness.G)
        S = []
        for g in G:
            inv_g = _get_inv(witness, g)
            fixes = True
            for x in X:
                if _get_f(witness, _get_action(witness, inv_g, x)) != _get_f(witness, x):
                    fixes = False
                    break
            if fixes:
                S.append(g)
        
        e = _get_id(witness, G)
        is_subgroup = True
        if e not in S:
            is_subgroup = False
        else:
            for g in S:
                if _get_inv(witness, g) not in S:
                    is_subgroup = False
                    break
            if is_subgroup:
                for g1 in S:
                    for g2 in S:
                        if _get_op(witness, g1, g2) not in S:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
        neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    r"H_1: Y is a set",
    r"H_2: Y^X is the set of all functions from X to Y",
    r"H_3: G acts on Y^X via (g \cdot f)(x) = f(g^{-1} \cdot x)",
    r"H_4: f is a function in Y^X",
    r"¬Q: The stabilizer of f in G is not the subgroup {g \in G \mid f(g^{-1} \cdot x) = f(x) for all x \in X}"
]

N_HYP = 4
NEG_Q_INDEX = 4