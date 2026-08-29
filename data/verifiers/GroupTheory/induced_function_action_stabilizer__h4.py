import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_valid_action(elements, identity, S, action_func):
    S_set = set(S)
    for s in S:
        try:
            res = action_func(identity, s)
            if res != s or res not in S_set:
                return False
        except Exception:
            return False
            
    is_left = True
    for s in S:
        for g1 in elements:
            for g2 in elements:
                try:
                    res2 = action_func(g2, s)
                    if res2 not in S_set:
                        is_left = False
                        break
                    res1 = action_func(g1, res2)
                    if res1 not in S_set:
                        is_left = False
                        break
                    res12 = action_func(g1 * g2, s)
                    if res12 not in S_set:
                        is_left = False
                        break
                    if res12 != res1:
                        is_left = False
                        break
                except Exception:
                    is_left = False
                    break
            if not is_left: break
        if not is_left: break

    is_right = True
    for s in S:
        for g1 in elements:
            for g2 in elements:
                try:
                    res1 = action_func(g1, s)
                    if res1 not in S_set:
                        is_right = False
                        break
                    res2 = action_func(g2, res1)
                    if res2 not in S_set:
                        is_right = False
                        break
                    res12 = action_func(g1 * g2, s)
                    if res12 not in S_set:
                        is_right = False
                        break
                    if res12 != res2:
                        is_right = False
                        break
                except Exception:
                    is_right = False
                    break
            if not is_right: break
        if not is_right: break

    return is_left or is_right

def conditions(witness):
    try:
        G = witness.get('G')
        X = witness.get('X')
        action_X = witness.get('action_X')
        Y = witness.get('Y')
        f = witness.get('f')
        action_Y = witness.get('action_Y')
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group acting on a set X
    h1 = False
    try:
        if isinstance(G, PermutationGroup) and isinstance(X, (list, set, tuple)):
            elements = list(G.generate())
            identity = G.identity
            if is_valid_action(elements, identity, X, action_X):
                h1 = True
    except Exception:
        h1 = False

    # H2: Y is a set
    h2 = False
    try:
        if isinstance(Y, (list, set, tuple)):
            h2 = True
    except Exception:
        h2 = False

    # H3: Y^X is the set of all functions from X to Y
    h3 = True

    # H4: f is a function in Y^X
    h4 = False
    try:
        Y_set = set(Y)
        if callable(f):
            h4 = True
            for x in X:
                val = f(x)
                if val not in Y_set:
                    h4 = False
                    break
        elif isinstance(f, dict):
            h4 = True
            for x in X:
                if x not in f or f[x] not in Y_set:
                    h4 = False
                    break
    except Exception:
        h4 = False

    # ¬Q: The stabilizer of f in G is not the subgroup {g \in G | f(g^{-1} \cdot x) = f(x) for all x \in X}
    neg_q = False
    try:
        if h1 and h2 and h4:
            def eval_f(x):
                return f(x) if callable(f) else f[x]

            claimed_stab = set()
            for g in elements:
                g_inv = g**-1
                is_in_stab = True
                for x in X:
                    if eval_f(action_X(g_inv, x)) != eval_f(x):
                        is_in_stab = False
                        break
                if is_in_stab:
                    claimed_stab.add(g)
            
            # The true stabilizer depends on the induced action. 
            # If the witness provides a non-trivial action of G on Y, the true stabilizer may differ.
            if action_Y is not None:
                if is_valid_action(elements, identity, Y, action_Y):
                    true_stab = set()
                    for g in elements:
                        g_inv = g**-1
                        is_in_stab = True
                        for x in X:
                            if action_Y(g, eval_f(action_X(g_inv, x))) != eval_f(x):
                                is_in_stab = False
                                break
                        if is_in_stab:
                            true_stab.add(g)
                    neg_q = (true_stab != claimed_stab)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: Y is a set",
    "H_3: Y^X is the set of all functions from X to Y",
    "H_4: f is a function in Y^X",
    "¬Q: The stabilizer of f in G is not the subgroup {g in G | f(g^-1 * x) = f(x) for all x in X}"
]

N_HYP = 4
NEG_Q_INDEX = 4