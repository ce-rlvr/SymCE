import math
import itertools
import sympy
from sympy import Rational

# Top-level setup
# (No special named objects required for this Real Analysis conjecture)

def conditions(witness) -> list[bool]:
    """
    witness can be either:
    (X, Y, Z, f, g, L_f, L_g)  # uses absolute difference as metric
    or
    (X, d_X, Y, d_Y, Z, d_Z, f, g, L_f, L_g) # uses custom metrics
    """
    try:
        if len(witness) == 7:
            X, Y, Z, f, g, L_f, L_g = witness
            d_X = lambda a, b: abs(a - b)
            d_Y = lambda a, b: abs(a - b)
            d_Z = lambda a, b: abs(a - b)
        elif len(witness) == 10:
            X, d_X, Y, d_Y, Z, d_Z, f, g, L_f, L_g = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    def eval_f(x):
        if isinstance(f, (dict, list, tuple)):
            return f[x]
        return f(x)
        
    def eval_g(y):
        if isinstance(g, (dict, list, tuple)):
            return g[y]
        return g(y)

    def dist(d, a, b):
        if isinstance(d, dict):
            return d[(a, b)]
        return d(a, b)

    def is_metric(space, d):
        try:
            for a, b in itertools.product(space, repeat=2):
                d_ab = dist(d, a, b)
                if d_ab < -1e-12: 
                    return False
                if a == b and abs(d_ab) > 1e-12: 
                    return False
                if a != b and d_ab <= 1e-12: 
                    return False
                if abs(dist(d, a, b) - dist(d, b, a)) > 1e-12: 
                    return False
                for c in space:
                    if dist(d, a, c) > dist(d, a, b) + dist(d, b, c) + 1e-9:
                        return False
            return True
        except Exception:
            return False

    # H1: f: X -> Y is Lipschitz continuous with constant L_f
    h1 = True
    try:
        if not is_metric(X, d_X): 
            h1 = False
        if not is_metric(Y, d_Y): 
            h1 = False
        if h1:
            for x in X:
                # Check if f maps X into Y
                if eval_f(x) not in Y:
                    h1 = False
                    break
        if h1:
            for x1, x2 in itertools.product(X, repeat=2):
                if dist(d_Y, eval_f(x1), eval_f(x2)) > L_f * dist(d_X, x1, x2) + 1e-9:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: g: Y -> Z is Lipschitz continuous with constant L_g
    h2 = True
    try:
        if not is_metric(Y, d_Y): 
            h2 = False
        if not is_metric(Z, d_Z): 
            h2 = False
        if h2:
            for y in Y:
                # Check if g maps Y into Z
                if eval_g(y) not in Z:
                    h2 = False
                    break
        if h2:
            for y1, y2 in itertools.product(Y, repeat=2):
                if dist(d_Z, eval_g(y1), eval_g(y2)) > L_g * dist(d_Y, y1, y2) + 1e-9:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: g o f is NOT Lipschitz continuous with constant L_f * L_g
    neg_q = False
    try:
        for x1, x2 in itertools.product(X, repeat=2):
            val1 = eval_g(eval_f(x1))
            val2 = eval_g(eval_f(x2))
            if dist(d_Z, val1, val2) > (L_f * L_g) * dist(d_X, x1, x2) + 1e-9:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous with constant L_f",
    "H_2: g is Lipschitz continuous with constant L_g",
    "¬Q: g o f is not Lipschitz continuous with constant L_f * L_g"
]

N_HYP = 2
NEG_Q_INDEX = 2