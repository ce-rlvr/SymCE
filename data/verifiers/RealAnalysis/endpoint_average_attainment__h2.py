import sympy as sp
from sympy.abc import x
import math

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        f, a, b = witness
        if not callable(f):
            f = sp.sympify(f)
    except Exception:
        return [False, False]

    # H1: f is a real-valued function defined on [a, b]
    h1 = False
    try:
        a_val = sp.sympify(a)
        b_val = sp.sympify(b)
        if a_val.is_real and b_val.is_real and a_val < b_val:
            h1 = True
            for i in range(101):
                c = float(a_val) + (float(b_val) - float(a_val)) * i / 100.0
                if callable(f):
                    try:
                        val = f(c)
                        if type(val) == complex and val.imag != 0:
                            h1 = False
                            break
                        if math.isnan(val) or math.isinf(val):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
                else:
                    free = f.free_symbols
                    var = list(free)[0] if len(free) == 1 else x
                    try:
                        val = f.subs(var, c)
                        float_val = float(val)
                        if math.isnan(float_val) or math.isinf(float_val):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
            
            if h1 and not callable(f):
                try:
                    free = f.free_symbols
                    var = list(free)[0] if len(free) == 1 else x
                    sings = sp.singularities(f, var)
                    if sings is not sp.S.EmptySet:
                        inter = sp.Intersection(sings, sp.Interval(a_val, b_val))
                        if inter is not sp.S.EmptySet:
                            h1 = False
                except Exception:
                    pass
    except Exception:
        h1 = False

    # neg_Q: There does NOT exist c in [a, b] such that f(c) = (f(a) + f(b)) / 2
    neg_q = False
    try:
        if callable(f):
            val_a = f(float(a_val))
            val_b = f(float(b_val))
            target = (val_a + val_b) / 2.0
            
            n_points = 100000
            min_dist = float('inf')
            step = (float(b_val) - float(a_val)) / n_points
            for i in range(n_points + 1):
                c = float(a_val) + i * step
                try:
                    val = f(c)
                    dist = abs(val - target)
                    if dist < min_dist:
                        min_dist = dist
                except Exception:
                    pass
            neg_q = min_dist > 1e-2
        else:
            free = f.free_symbols
            var = list(free)[0] if len(free) == 1 else x
            val_a = f.subs(var, a_val)
            val_b = f.subs(var, b_val)
            target = (val_a + val_b) / 2
            
            # Try solveset first
            sols = sp.solveset(sp.Eq(f, target), var, domain=sp.Interval(a_val, b_val))
            if sols is sp.S.EmptySet:
                neg_q = True
            elif isinstance(sols, sp.FiniteSet):
                if len(sols) == 0:
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Fallback to lambdify and grid search
                try:
                    f_lam = sp.lambdify(var, f, 'math')
                    n_points = 100000
                    min_dist = float('inf')
                    step = (float(b_val) - float(a_val)) / n_points
                    target_float = float(target)
                    for i in range(n_points + 1):
                        c = float(a_val) + i * step
                        try:
                            val = f_lam(c)
                            dist = abs(val - target_float)
                            if dist < min_dist:
                                min_dist = dist
                        except Exception:
                            pass
                    neg_q = min_dist > 1e-2
                except Exception:
                    # If lambdify fails, use subs with fewer points
                    n_points = 1000
                    min_dist = float('inf')
                    step = (float(b_val) - float(a_val)) / n_points
                    target_float = float(target)
                    for i in range(n_points + 1):
                        c = float(a_val) + i * step
                        try:
                            val = f.subs(var, c)
                            dist = abs(float(val) - target_float)
                            if dist < min_dist:
                                min_dist = dist
                        except Exception:
                            pass
                    neg_q = min_dist > 1e-2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval a to b",
    "¬Q: There does not exist c in a to b such that f(c) = (f(a) + f(b)) / 2"
]

N_HYP = 1
NEG_Q_INDEX = 1