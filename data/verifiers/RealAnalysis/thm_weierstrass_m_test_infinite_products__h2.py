import sympy
from sympy.abc import n, x
import math

def h1_check(witness):
    f = witness.get('f')
    X = witness.get('X')
    if f is None or X is None:
        return False
        
    try:
        pts = list(X)
    except TypeError:
        if hasattr(X, 'start') and hasattr(X, 'end'):
            pts = []
            if X.start.is_finite: pts.append(X.start)
            if X.end.is_finite: pts.append(X.end)
            if not pts: pts.append(0.0)
        else:
            pts = [0.0]
            
    for pt in pts:
        for n_val in [1, 2, 3]:
            val = f.subs({n: n_val, x: pt})
            try:
                v = float(val)
                if math.isinf(v) or math.isnan(v):
                    return False
            except (TypeError, ValueError):
                return False
    return True

def h2_check(witness):
    M = witness.get('M')
    if M is None:
        return False
    S = sympy.Sum(M, (n, 1, sympy.oo))
    if S.is_convergent() is True:
        return True
    val = S.doit()
    if val.is_finite:
        return True
    return False

def neg_q_check(witness):
    f = witness.get('f')
    X = witness.get('X')
    if f is None or X is None:
        return False
        
    try:
        pts = list(X)
    except TypeError:
        if hasattr(X, 'start') and hasattr(X, 'end'):
            pts = []
            if X.start.is_finite: pts.append(X.start)
            if X.end.is_finite: pts.append(X.end)
            if X.start.is_finite and X.end.is_finite:
                pts.append((X.start + X.end)/2)
            if not pts: pts.append(0.0)
        else:
            pts = [0.0]
            
    for pt in pts:
        f_sub = f.subs(x, pt)
        
        # Check limit of f_n as n -> oo
        L = sympy.limit(f_sub, n, sympy.oo)
        if L != 0:
            return True
            
        # Check sum of f_n
        S = sympy.Sum(f_sub, (n, 1, sympy.oo)).doit()
        if S == sympy.oo or S == -sympy.oo:
            return True
            
        # Check product of (1 + f_n)
        P = sympy.Product(1 + f_sub, (n, 1, sympy.oo)).doit()
        if P == sympy.oo or P == -sympy.oo or P == 0:
            return True
            
    return False

def conditions(witness):
    try:
        h1 = h1_check(witness)
    except Exception:
        h1 = False

    try:
        h2 = h2_check(witness)
    except Exception:
        h2 = False

    try:
        neg_q = neg_q_check(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on a set X",
    "H_2: The infinite series \\sum_{n=1}^\\infty M_n converges",
    "¬Q: The infinite product \\prod_{n=1}^\\infty (1 + f_n(x)) does NOT converge uniformly on X"
]

N_HYP = 2
NEG_Q_INDEX = 2