import sympy
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup
# For finite rings Z_n, use integers to represent the ring.
# e.g., R = 6 represents Z_6.
# f can be a dictionary mapping elements 0..R-1 to 0..S-1.
# M can be a list of elements in R.

def conditions(witness):
    try:
        S = witness['S']
        if isinstance(S, (int, Integer)):
            h1 = (S >= 2)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        R = witness['R']
        S = witness['S']
        f = witness['f']
        
        if isinstance(R, (int, Integer)) and isinstance(S, (int, Integer)):
            if isinstance(f, dict):
                f_eval = lambda x: f.get(x, None)
            elif isinstance(f, (list, tuple)):
                f_eval = lambda x: f[x] if x < len(f) else None
            else:
                f_eval = lambda x: f(x)
                
            h2 = True
            for a in range(R):
                fa = f_eval(a)
                if fa is None or not (isinstance(fa, (int, Integer)) and 0 <= fa < S):
                    h2 = False
                    break
                for b in range(R):
                    fb = f_eval(b)
                    fab_add = f_eval((a + b) % R)
                    fab_mul = f_eval((a * b) % R)
                    if fab_add != (fa + fb) % S:
                        h2 = False
                        break
                    if fab_mul != (fa * fb) % S:
                        h2 = False
                        break
                if not h2:
                    break
            if h2:
                if f_eval(1 % R) != 1 % S:
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        R = witness['R']
        f = witness['f']
        M = witness['M']
        
        if isinstance(R, (int, Integer)):
            if isinstance(f, dict):
                f_eval = lambda x: f.get(x, None)
            elif isinstance(f, (list, tuple)):
                f_eval = lambda x: f[x] if x < len(f) else None
            else:
                f_eval = lambda x: f(x)
                
            if isinstance(M, (list, tuple, set, dict)):
                in_M = lambda x: x in M
            else:
                in_M = lambda x: M(x)
                
            neg_q = False
            for x in range(R):
                if f_eval(x) == 0:
                    if not in_M(x):
                        neg_q = True
                        break
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a non-zero ring",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: The kernel of f is not a subset of M"
]

N_HYP = 2
NEG_Q_INDEX = 2