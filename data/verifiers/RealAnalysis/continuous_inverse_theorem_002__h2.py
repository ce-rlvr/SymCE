import sympy
from sympy import Interval, Symbol, S
from sympy.calculus.util import continuous_domain
from sympy.abc import x, y, z
import math
import itertools
import functools

def get_var(f):
    if hasattr(f, 'free_symbols'):
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            return list(free_syms)[0]
    return x

def conditions(witness):
    """
    witness is expected to be a tuple (f, I)
    where f is a sympy expression and I is a sympy Interval.
    """
    try:
        f, I = witness
    except Exception:
        return [False, False, False]
        
    # H_1: I is an interval in R
    try:
        h1 = isinstance(I, sympy.Interval) and bool(I.start < I.end)
    except Exception:
        h1 = False
        
    # H_2: f is continuous on I
    try:
        var = get_var(f)
        dom = continuous_domain(f, var, S.Reals)
        h2 = bool(I.is_subset(dom))
    except Exception:
        h2 = False
        
    # ¬Q: The inverse function f^-1 is not continuous on the image interval f(I)
    # For a continuous function on an interval, this happens iff f is NOT injective.
    try:
        neg_q = False
        if h1:
            var = get_var(f)
            a = I.start if I.start.is_finite else -sympy.Integer(100)
            b = I.end if I.end.is_finite else sympy.Integer(100)
            
            # Generate test points in the interval
            points = []
            for i in range(1001):
                p = a + sympy.Rational(i, 1000) * (b - a)
                if I.contains(p):
                    points.append(p)
                    
            if len(points) >= 2:
                vals = []
                valid_points = []
                for p in points:
                    try:
                        val = f.subs(var, p)
                        v = float(val)
                        vals.append(v)
                        valid_points.append(p)
                    except Exception:
                        pass
                points = valid_points
                
                if len(vals) >= 2:
                    direction = 0
                    reversed_dir = False
                    # Check for strict monotonicity
                    for i in range(len(vals) - 1):
                        diff = vals[i+1] - vals[i]
                        if abs(diff) > 1e-10:
                            if direction == 0:
                                direction = 1 if diff > 0 else -1
                            else:
                                if (diff > 0 and direction == -1) or (diff < 0 and direction == 1):
                                    reversed_dir = True
                                    break
                                    
                    if reversed_dir:
                        neg_q = True
                    else:
                        # Check if endpoints map to the same value
                        val_start = f.subs(var, points[0])
                        val_end = f.subs(var, points[-1])
                        try:
                            if val_start == val_end:
                                neg_q = True
                        except Exception:
                            pass
                            
                        if not neg_q:
                            try:
                                if sympy.simplify(val_start - val_end) == 0:
                                    neg_q = True
                            except Exception:
                                pass
                                
                        if not neg_q:
                            # Check inner points for flatness (constant subintervals)
                            simplify_calls = 0
                            for i in range(len(vals)):
                                if neg_q or simplify_calls > 100: break
                                for j in range(i + 10, len(vals)):
                                    if abs(vals[i] - vals[j]) < 1e-12:
                                        vi = f.subs(var, points[i])
                                        vj = f.subs(var, points[j])
                                        try:
                                            if vi == vj:
                                                neg_q = True
                                                break
                                        except Exception:
                                            pass
                                            
                                        if not neg_q:
                                            try:
                                                simplify_calls += 1
                                                if sympy.simplify(vi - vj) == 0:
                                                    neg_q = True
                                                    break
                                            except Exception:
                                                pass
                                        if simplify_calls > 100:
                                            break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an interval in R",
    "H_2: f is continuous on I",
    "¬Q: The inverse function f^-1 is not continuous on the image interval f(I) (f is not injective)"
]

N_HYP = 2
NEG_Q_INDEX = 2