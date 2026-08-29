import sympy
import sympy.abc
from sympy import pi, Interval, Symbol
from sympy.calculus.util import continuous_domain
import math

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    if callable(witness):
        try:
            f_expr = witness(x)
        except Exception:
            return [False, False]
    else:
        f_expr = witness

    # H1: f is 2*pi-periodic
    h1_ok = False
    try:
        # Evaluate at several points to check periodicity
        points = [-3.14159, -2.718, -1.0, 0.0, 1.0, 2.718, 3.14159, 5.0, 10.0]
        is_per = True
        success_count = 0
        for p in points:
            try:
                v1 = float(f_expr.subs(x, p).evalf())
                v2 = float(f_expr.subs(x, p + 2*pi).evalf())
                success_count += 1
                if abs(v1 - v2) > 1e-4:
                    is_per = False
                    break
            except Exception:
                continue
        h1_ok = is_per and (success_count > 0)
    except Exception:
        h1_ok = False

    # neg_Q: The Fourier series of f does not converge uniformly to f on R
    # A necessary condition for uniform convergence to f is that f is continuous.
    # We check if f has any discontinuities on [-pi, pi].
    neg_q_ok = False
    cd_failed = False
    try:
        cd = continuous_domain(f_expr, x, Interval.open(-pi, pi))
        if not Interval.open(-pi, pi).is_subset(cd):
            neg_q_ok = True
    except Exception:
        cd_failed = True

    if not cd_failed and not neg_q_ok:
        try:
            # Check for boundary mismatch (jump at odd multiples of pi)
            lim_left = f_expr.limit(x, pi, '-')
            lim_right = f_expr.limit(x, -pi, '+')
            try:
                diff = float(abs(lim_left - lim_right).evalf())
                if diff > 1e-5:
                    neg_q_ok = True
            except Exception:
                if lim_left != lim_right:
                    neg_q_ok = True
        except Exception:
            # Fallback for limit evaluation failure
            try:
                v_left = float(f_expr.subs(x, math.pi - 1e-5).evalf())
                v_right = float(f_expr.subs(x, -math.pi + 1e-5).evalf())
                if abs(v_left - v_right) > 1e-3:
                    neg_q_ok = True
            except Exception:
                pass

    # Numerical fallback if continuous_domain fails
    if cd_failed and not neg_q_ok:
        try:
            points_num = [ -math.pi + i*2*math.pi/1000 for i in range(1001) ]
            vals = []
            for p in points_num:
                v = float(f_expr.subs(x, p).evalf())
                vals.append(v)
            
            # Check boundary match
            if abs(vals[0] - vals[-1]) > 1e-4:
                neg_q_ok = True
            else:
                # Check for internal jumps
                diffs = [abs(vals[i] - vals[i+1]) for i in range(len(vals)-1)]
                max_diff = max(diffs)
                diffs.sort()
                median_diff = diffs[len(diffs)//2]
                if max_diff > 0.1 and max_diff > 100 * median_diff:
                    neg_q_ok = True
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a 2*pi-periodic function",
    "¬Q: The Fourier series of f does not converge uniformly to f on R"
]

N_HYP = 1
NEG_Q_INDEX = 1