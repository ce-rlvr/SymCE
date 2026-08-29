import sympy
from sympy import Symbol, Expr
from sympy.abc import x, y
import math
import itertools
import functools

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Check if witness is a string describing a known counterexample
    if isinstance(witness, str):
        s = witness.lower()
        if ("conway" in s and "13" in s) or \
           ("base" in s and "13" in s) or \
           ("q-linear" in s and "surjective" in s) or \
           ("q linear" in s and "surjective" in s) or \
           ("hamel" in s) or \
           ("nowhere continuous open map" in s):
            return [True, True]
            
    # 2. Check if witness is a class or function named after a known counterexample
    name = getattr(witness, '__name__', '')
    if not name and hasattr(witness, '__class__'):
        name = witness.__class__.__name__
    name = name.lower()
    if ("conway" in name and "13" in name) or \
       ("base" in name and "13" in name) or \
       ("qlinear" in name and "surjective" in name):
        return [True, True]

    # 3. Check if witness is a mock object with explicit attributes
    if hasattr(witness, 'is_open_map'):
        try:
            val = witness.is_open_map() if callable(witness.is_open_map) else witness.is_open_map
            h1 = bool(val)
        except Exception:
            pass
            
    if hasattr(witness, 'is_strictly_monotonic'):
        try:
            val = witness.is_strictly_monotonic() if callable(witness.is_strictly_monotonic) else witness.is_strictly_monotonic
            neg_q = not bool(val)
        except Exception:
            pass

    # 4. Empirical check for strict monotonicity if not already determined
    if not neg_q:
        vals = None
        try:
            pts = [-10.0, -5.0, -1.0, 0.0, 1.0, 5.0, 10.0]
            if callable(witness):
                vals = [float(witness(p)) for p in pts]
            elif isinstance(witness, Expr):
                free_syms = witness.free_symbols
                if len(free_syms) == 1:
                    sym = list(free_syms)[0]
                    vals = [float(witness.subs(sym, p)) for p in pts]
                elif len(free_syms) == 0:
                    vals = [float(witness)] * len(pts)
            
            if vals is not None:
                inc = all(vals[i] < vals[i+1] for i in range(len(vals)-1))
                dec = all(vals[i] > vals[i+1] for i in range(len(vals)-1))
                if not (inc or dec):
                    neg_q = True
        except Exception:
            pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: For every open set U \\subseteq \\mathbb{R}, the image f(U) is an open set in \\mathbb{R}",
    "¬Q: f is not strictly monotonic on \\mathbb{R}"
]

N_HYP = 1
NEG_Q_INDEX = 1