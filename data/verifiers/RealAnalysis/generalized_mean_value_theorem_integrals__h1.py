import sympy
from sympy import Piecewise, Interval, integrate, solveset, S
from sympy.calculus.util import minimum, maximum
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        f = witness.get('f')
        g = witness.get('g')
        a = witness.get('a')
        b = witness.get('b')
    else:
        f, g, a, b = witness

    try:
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]

    # H1: g(x) does not change sign on interval a to b
    def check_h1():
        try:
            ivl = Interval(a, b)
            min_val = minimum(g, x, ivl)
            max_val = maximum(g, x, ivl)
            if min_val >= 0 or max_val <= 0:
                return True
            if min_val < 0 and max_val > 0:
                return False
        except Exception:
            pass
        
        try:
            vals = []
            n_samples = 1000
            a_f = float(a)
            b_f = float(b)
            for i in range(n_samples + 1):
                val = a_f + (b_f - a_f) * i / n_samples
                v = float(g.subs(x, val))
                vals.append(v)
            has_pos = any(v > 1e-9 for v in vals)
            has_neg = any(v < -1e-9 for v in vals)
            if has_pos and has_neg:
                return False
            return True
        except Exception:
            return False

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    # H2: a < b
    try:
        h2 = bool(float(a) < float(b))
    except Exception:
        h2 = False

    # neg_Q: For all c in interval a to b, int f*g != f(c) * int g
    def check_neg_Q():
        target_f = None
        try:
            L_val = integrate(f * g, (x, a, b))
            R_int_val = integrate(g, (x, a, b))
            
            if float(R_int_val) == 0.0:
                if float(L_val) == 0.0:
                    return False
                else:
                    return True
                    
            target = L_val / R_int_val
            target_f = float(target)
            
            sols = solveset(f - target, x, domain=Interval.open(a, b))
            if sols is S.EmptySet:
                return True
            if sols is not S.EmptySet and not isinstance(sols, sympy.ConditionSet):
                return False
        except Exception:
            pass
            
        # Fallback to dense sampling and bisection for root finding
        try:
            a_f = float(a)
            b_f = float(b)
            
            if target_f is None:
                sum_fg = 0.0
                sum_g = 0.0
                n_int = 1000
                dx = (b_f - a_f) / n_int
                for i in range(n_int):
                    xi = a_f + (i + 0.5) * dx
                    vi_f = float(f.subs(x, xi))
                    vi_g = float(g.subs(x, xi))
                    sum_fg += vi_f * vi_g * dx
                    sum_g += vi_g * dx
                if abs(sum_g) < 1e-9:
                    if abs(sum_fg) < 1e-9:
                        return False
                    else:
                        return True
                target_f = sum_fg / sum_g

            n_samples = 10000
            prev_diff = None
            prev_x = None
            
            for i in range(1, n_samples):
                curr_x = a_f + (b_f - a_f) * i / n_samples
                try:
                    v = float(f.subs(x, curr_x))
                    diff = v - target_f
                    if abs(diff) < 1e-5:
                        return False
                    if prev_diff is not None and prev_x is not None:
                        if prev_diff * diff < 0:
                            # Sign change detected. Bisection to distinguish jump from continuous crossing.
                            left_x = prev_x
                            right_x = curr_x
                            left_diff = prev_diff
                            for _ in range(40):
                                mid_x = (left_x + right_x) / 2.0
                                try:
                                    mid_v = float(f.subs(x, mid_x))
                                    mid_diff = mid_v - target_f
                                    if abs(mid_diff) < 1e-5:
                                        return False
                                    if left_diff * mid_diff <= 0:
                                        right_x = mid_x
                                    else:
                                        left_x = mid_x
                                        left_diff = mid_diff
                                except Exception:
                                    break
                    prev_diff = diff
                    prev_x = curr_x
                except Exception:
                    prev_diff = None
                    prev_x = None
            return True
        except Exception:
            return False

    try:
        neg_q = check_neg_Q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: g(x) does not change sign on interval a to b",
    "H_2: a < b",
    "not Q: There is no c in interval a to b such that integral of f*g equals f(c) times integral of g"
]

N_HYP = 2
NEG_Q_INDEX = 2