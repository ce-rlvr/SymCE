import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def get_attr(obj, attr):
    if isinstance(obj, dict):
        return obj[attr]
    return getattr(obj, attr)

def conditions(witness) -> list[bool]:
    try:
        G = get_attr(witness, 'G')
        mul = get_attr(witness, 'mul')
        inv = get_attr(witness, 'inv')
        e = get_attr(witness, 'e')
        X = get_attr(witness, 'X')
        Y = get_attr(witness, 'Y')
        action = get_attr(witness, 'action')
    except Exception:
        return [False, False, False]

    # H1: G is a group acting on a set X.
    try:
        is_group = True
        G_list = list(G)
        if e not in G_list:
            is_group = False
        else:
            for g in G_list:
                if mul(g, e) != g or mul(e, g) != g:
                    is_group = False
                if mul(g, inv(g)) != e or mul(inv(g), g) != e:
                    is_group = False
            for g1 in G_list:
                for g2 in G_list:
                    if mul(g1, g2) not in G_list:
                        is_group = False
                    for g3 in G_list:
                        if mul(g1, mul(g2, g3)) != mul(mul(g1, g2), g3):
                            is_group = False

        is_action = False
        if is_group:
            X_list = list(X)
            closed = all(action(g, x) in X_list for g in G_list for x in X_list)
            if closed:
                id_pres = all(action(e, x) == x for x in X_list)
                # A valid group action can be either a left action or a right action.
                is_left = all(action(mul(g1, g2), x) == action(g1, action(g2, x)) for g1 in G_list for g2 in G_list for x in X_list)
                is_right = all(action(mul(g1, g2), x) == action(g2, action(g1, x)) for g1 in G_list for g2 in G_list for x in X_list)
                if id_pres and (is_left or is_right):
                    is_action = True
        h1 = is_group and is_action
    except Exception:
        h1 = False

    # H2: Y^X is the set of all functions from X to Y.
    try:
        # This is a definitional hypothesis; we just verify X and Y are valid collections.
        h2 = hasattr(X, '__iter__') and hasattr(Y, '__iter__')
    except Exception:
        h2 = False

    # neg_Q: The operation is NOT a valid group action of G on Y^X.
    try:
        valid_action = True
        G_list = list(G)
        X_list = list(X)
        Y_list = list(Y)
        
        # A valid group action on Y^X must be a left action, meaning:
        # induced(g1 * g2, f) == induced(g1, induced(g2, f))
        # where induced(g, f)(x) = f(action(inv(g), x)).
        # This requires action(inv(g1 * g2), x) == action(inv(g2), action(inv(g1), x)) for all x.
        # If this fails for some x, and Y has at least 2 elements, we can construct an f that distinguishes them.
        for g1 in G_list:
            for g2 in G_list:
                for x in X_list:
                    x_lhs = action(inv(g2), action(inv(g1), x))
                    x_rhs = action(inv(mul(g1, g2)), x)
                    if x_lhs != x_rhs:
                        if len(Y_list) >= 2:
                            valid_action = False
                            break
                if not valid_action:
                    break
            if not valid_action:
                break
        neg_q = not valid_action
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y^X is the set of all functions from X to Y",
    "¬Q: The induced operation is not a valid group action of G on Y^X"
]

N_HYP = 2
NEG_Q_INDEX = 2