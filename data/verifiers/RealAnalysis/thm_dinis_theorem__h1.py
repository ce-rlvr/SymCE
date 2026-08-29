import sympy
from sympy import S, Interval, Union, FiniteSet, oo, diff, solveset, limit, Abs
from sympy.calculus.util import continuous_domain
import math

# Top-level setup
x, n = sympy.symbols('x n', real=True)

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of continuous functions from K to the real numbers",
    "H_2: For each x in K, the sequence of real numbers (f_n(x)) is monotonically decreasing",
    "H_3: The sequence (f_n) converges pointwise to a continuous function f on K",
    "¬Q: The sequence (f_n) does not converge uniformly to f on K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def sample_points(K):
    if K == S.Reals:
        K = Interval(-oo, oo)
    pts = []
    if isinstance(K, Interval):
        start = float(K.start) if K.start != -oo else -100.0
        end = float(K.end) if K.end != oo else 100.0
        for i in range(1, 100):
            pts.append(start + i * (end - start) / 100)
        if K.left_open and K.start != -oo:
            pts.append(start + 1e-4)
            pts.append(start + 1e-6)
            pts.append(start + 1e-8)
        if K.right_open and K.end != oo:
            pts.append(end - 1e-4)
            pts.append(end - 1e-6)
            pts.append(end - 1e-8)
        if K.end == oo:
            pts.extend([10.0**i for i in range(1, 8)])
        if K.start == -oo:
            pts.extend([-10.0**i for i in range(1, 8)])
    elif isinstance(K, Union):
        for arg in K.args:
            pts.extend(sample_points(arg))
    elif isinstance(K, FiniteSet):
        for arg in K.args:
            pts.append(float(arg))
    return pts

def conditions(witness):
    try:
        K, f_n, f, w_x, w_n = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: f_n is continuous on K
    h1 = True
    try:
        for i in [1, 2, 5]:
            f_i = f_n.subs(w_n, i)
            try:
                dom = continuous_domain(f_i, w_x, S.Reals)
                if not K.is_subset(dom):
                    h1 = False
                    break
            except Exception:
                pts = sample_points(K)
                for p in pts:
                    try:
                        val = complex(f_i.subs(w_x, p))
                        if val.imag != 0 or math.isnan(val.real) or math.isinf(val.real):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: f_n(x) is monotonically decreasing
    h2 = True
    try:
        for i in range(1, 6):
            diff_expr = f_n.subs(w_n, i) - f_n.subs(w_n, i+1)
            try:
                pts = sample_points(K)
                for p in pts:
                    try:
                        if float(diff_expr.subs(w_x, p)) < -1e-7:
                            h2 = False
                            break
                    except Exception:
                        pass
                
                if not h2:
                    break

                deriv = diff(diff_expr, w_x)
                crit_points = solveset(deriv, w_x, domain=K)
                if isinstance(crit_points, FiniteSet):
                    for p in crit_points:
                        try:
                            if float(diff_expr.subs(w_x, p)) < -1e-7:
                                h2 = False
                                break
                        except Exception:
                            pass
            except Exception:
                pass
            if not h2:
                break
    except Exception:
        h2 = False

    # H3: f_n converges pointwise to continuous f on K
    h3 = True
    try:
        try:
            dom_f = continuous_domain(f, w_x, S.Reals)
            if not K.is_subset(dom_f):
                h3 = False
        except Exception:
            pts = sample_points(K)
            for p in pts:
                try:
                    val = complex(f.subs(w_x, p))
                    if val.imag != 0 or math.isnan(val.real) or math.isinf(val.real):
                        h3 = False
                        break
                except Exception:
                    h3 = False
                    break

        if h3:
            fallback_needed = False
            try:
                lim_f = limit(f_n, w_n, oo)
                pts = sample_points(K)
                success_count = 0
                for p in pts:
                    try:
                        val_lim = float(lim_f.subs(w_x, p))
                        val_f = float(f.subs(w_x, p))
                        if abs(val_lim - val_f) > 1e-5:
                            h3 = False
                            break
                        success_count += 1
                    except Exception:
                        pass
                if success_count == 0:
                    fallback_needed = True
            except Exception:
                fallback_needed = True
                
            if fallback_needed and h3:
                pts = sample_points(K)
                success_count = 0
                for p in pts:
                    try:
                        val_f = float(f.subs(w_x, p))
                        converged = False
                        for large_n in [1000, 10000, 100000, 1000000]:
                            val_n = float(f_n.subs({w_x: p, w_n: large_n}))
                            if abs(val_n - val_f) <= 1e-2:
                                converged = True
                                break
                        if not converged:
                            h3 = False
                            break
                        success_count += 1
                    except Exception:
                        pass
                if success_count == 0:
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: f_n does NOT converge uniformly to f on K
    neg_q = False
    try:
        sups = []
        for i in [10, 100, 1000, 10000]:
            expr = Abs(f_n.subs(w_n, i) - f)
            pts = sample_points(K)
            try:
                inside = f_n.subs(w_n, i) - f
                deriv = diff(inside, w_x)
                crit_points = solveset(deriv, w_x, domain=K)
                if isinstance(crit_points, FiniteSet):
                    for p in crit_points:
                        pts.append(float(p))
            except Exception:
                pass
            
            valid_vals = []
            for p in pts:
                try:
                    valid_vals.append(float(expr.subs(w_x, p)))
                except Exception:
                    pass
            if not valid_vals:
                break
            M = max(valid_vals)
            sups.append(M)
        
        # If the supremum does not converge to 0, uniform convergence fails.
        if len(sups) == 4 and sups[-1] > 1e-5 and sups[-1] >= 0.2 * sups[0]:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]