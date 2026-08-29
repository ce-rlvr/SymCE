import sympy as sp
from sympy import Symbol, Interval, S, limit, oo
import math

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def check_converges_on_D(X, D, f):
    if D != 'Q':
        return False
    
    points = []
    for den in range(1, 6):
        for num in range(-den*10, den*10 + 1):
            pt = S(num)/den
            if pt in X:
                points.append(pt)
                
    # Sort to ensure deterministic behavior
    points = sorted(list(set(points)), key=lambda p: float(p))
    
    # Limit to 15 points to be fast, but spread them out
    if len(points) > 15:
        step = len(points) / 15.0
        points = [points[int(i * step)] for i in range(15)]
        
    if not points:
        return False
        
    for pt in points:
        try:
            expr = f.subs(x, pt)
            L = limit(expr, n, oo)
            if "Limit" in str(type(L)):
                raise ValueError("Unevaluated limit")
            if L.is_finite is False or L.has(oo, -oo) or "AccumBounds" in str(type(L)):
                return False
        except Exception:
            try:
                val1 = float(f.subs({x: pt, n: 10000}))
                val2 = float(f.subs({x: pt, n: 10001}))
                if math.isnan(val1) or math.isnan(val2):
                    return False
                if abs(val1 - val2) > 1e-3:
                    return False
            except Exception:
                return False
    return True

def check_neg_Q(X, D, f):
    try:
        inf = float(X.inf) if X.inf != S.NegativeInfinity else -10.0
        sup = float(X.sup) if X.sup != S.Infinity else 10.0
    except Exception:
        inf, sup = 0.0, 1.0
        
    points = [inf + (sup - inf) * i / 100.0 for i in range(101)]
    points += [0.0, 1.0, -1.0, 0.5, -0.5, 1/3, 2/3]
    
    valid_points = []
    for p in points:
        try:
            if p >= inf and p <= sup:
                valid_points.append(p)
        except Exception:
            pass
            
    unique_points = {}
    for p in valid_points:
        unique_points[round(float(p), 7)] = p
    points = sorted(list(unique_points.values()), key=lambda p: float(p))
    
    limits = {}
    for p in points:
        try:
            expr = f.subs(x, p)
            L = limit(expr, n, oo)
            if "Limit" in str(type(L)):
                raise ValueError("Unevaluated limit")
            if L.is_finite is False or L.has(oo, -oo) or "AccumBounds" in str(type(L)):
                return True # Diverges, so conclusion fails
            limits[p] = float(L)
        except Exception:
            try:
                val1 = float(f.subs({x: p, n: 10000}))
                val2 = float(f.subs({x: p, n: 10001}))
                if math.isnan(val1) or math.isnan(val2):
                    return True
                if abs(val1 - val2) > 1e-3:
                    return True
                limits[p] = val2
            except Exception:
                return True
                
    # Check continuity of the limit function
    threshold = (sup - inf) / 50.0 + 1e-5
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        if abs(p1 - p2) < threshold:
            diff = abs(limits[p1] - limits[p2])
            if diff > 0.1:
                # Zoom in using bisection to confirm it's a true discontinuity (step) 
                # rather than just a steep continuous slope.
                left, right = p1, p2
                vleft, vright = limits[p1], limits[p2]
                current_diff = diff
                for _ in range(5):
                    pmid = (left + right) / 2.0
                    try:
                        expr = f.subs(x, pmid)
                        L = limit(expr, n, oo)
                        if "Limit" in str(type(L)):
                            raise ValueError
                        if L.is_finite is False or L.has(oo, -oo) or "AccumBounds" in str(type(L)):
                            return True
                        vmid = float(L)
                    except Exception:
                        try:
                            vmid = float(f.subs({x: pmid, n: 10001}))
                        except Exception:
                            return True
                            
                    diff1 = abs(vleft - vmid)
                    diff2 = abs(vmid - vright)
                    if diff1 > diff2:
                        right = pmid
                        vright = vmid
                        current_diff = diff1
                    else:
                        left = pmid
                        vleft = vmid
                        current_diff = diff2
                        
                # If it's a true discontinuity, the jump size remains large.
                if current_diff > diff * 0.8:
                    return True
                    
    return False

def conditions(witness) -> list[bool]:
    try:
        X, D, f = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if callable(f):
            f = f(n, x)
    except Exception:
        pass
        
    try:
        h1 = isinstance(X, sp.Set) and X.is_subset(S.Reals)
    except Exception:
        h1 = False
        
    try:
        if D == 'Q':
            if X == S.Reals:
                h2 = True
            elif isinstance(X, sp.Interval):
                h2 = X.measure > 0
            elif isinstance(X, sp.Union):
                h2 = any(isinstance(arg, sp.Interval) and arg.measure > 0 for arg in X.args)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        h3 = check_converges_on_D(X, D, f)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(X, D, f)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: D is a dense subset of X",
    "H_3: The sequence (f_n(x)) converges for each x in D",
    "¬Q: The sequence (f_n) does not converge pointwise everywhere on X to a continuous function"
]

N_HYP = 3
NEG_Q_INDEX = 3