import sympy
from sympy import symbols
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: X is a compact metric space with metric d",
    "H_2: f: X -> X is a mapping",
    "¬Q: f does not have a unique fixed point"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            X_raw = list(witness.keys())
            d = lambda u, v: 0.0 if u == v else 1.0
            f = lambda u: witness[u]
        elif isinstance(witness, tuple) and len(witness) == 2:
            X, f_obj = witness
            X_raw = list(X)
            d = lambda u, v: 0.0 if u == v else 1.0
            if isinstance(f_obj, dict):
                f = lambda u: f_obj[u]
            elif isinstance(f_obj, (list, tuple)):
                f = lambda u: f_obj[u]
            else:
                f = f_obj
        elif isinstance(witness, tuple) and len(witness) == 3:
            X, d_obj, f_obj = witness
            X_raw = list(X)
            
            if isinstance(d_obj, dict):
                d = lambda u, v: float(d_obj.get((u, v), d_obj.get((v, u), 0.0)))
            else:
                d = d_obj
                
            if isinstance(f_obj, dict):
                f = lambda u: f_obj[u]
            elif isinstance(f_obj, (list, tuple)):
                f = lambda u: f_obj[u]
            else:
                f = f_obj
        elif hasattr(witness, 'X') and hasattr(witness, 'f'):
            X_raw = list(witness.X)
            if hasattr(witness, 'd'):
                d_obj = witness.d
                if isinstance(d_obj, dict):
                    d = lambda u, v: float(d_obj.get((u, v), d_obj.get((v, u), 0.0)))
                else:
                    d = d_obj
            else:
                d = lambda u, v: 0.0 if u == v else 1.0
                
            f_obj = witness.f
            if isinstance(f_obj, dict):
                f = lambda u: f_obj[u]
            elif isinstance(f_obj, (list, tuple)):
                f = lambda u: f_obj[u]
            else:
                f = f_obj
        else:
            return [False, False, False]

        X_list = []
        for item in X_raw:
            if item not in X_list:
                X_list.append(item)
                
        # Check H1: X is a compact metric space with metric d
        # We restrict to finite spaces (which are always compact) of reasonable size to ensure fast verification
        if 0 < len(X_list) <= 200:
            h1 = True
            for u in X_list:
                for v in X_list:
                    dist = float(d(u, v))
                    if dist < 0:
                        h1 = False
                        break
                    if (dist == 0) != (u == v):
                        h1 = False
                        break
                    if abs(dist - float(d(v, u))) > 1e-7:
                        h1 = False
                        break
                    for w in X_list:
                        if dist > float(d(u, w)) + float(d(w, v)) + 1e-7:
                            h1 = False
                            break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        # Check H2: f: X -> X is a mapping
        if h1:
            h2 = True
            for u in X_list:
                if f(u) not in X_list:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        # Check neg_Q: There does NOT exist a unique x in X such that f(x) == x
        if h1 and h2:
            fixed_points = 0
            for u in X_list:
                if f(u) == u:
                    fixed_points += 1
            neg_q = (fixed_points != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]