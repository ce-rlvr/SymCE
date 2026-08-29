import sympy
from sympy.abc import x
import math

def conditions(witness):
    # H_1: f is a continuous real-valued function on the closed interval 0 to 1
    h1_ok = False
    try:
        f = witness
        is_continuous = True
        try:
            sings = sympy.singularities(f, x)
            inter = sympy.Intersection(sings, sympy.Interval(0, 1))
            if inter != sympy.S.EmptySet:
                is_continuous = False
        except Exception:
            pass

        if is_continuous:
            for pt in [0, 0.25, 0.5, 0.75, 1]:
                v = f.subs(x, pt)
                try:
                    v_float = float(v)
                except (TypeError, ValueError):
                    is_continuous = False
                    break
                
                if pt > 0:
                    L_left = sympy.limit(f, x, pt, dir='-')
                    try:
                        if abs(float(L_left) - v_float) > 1e-7:
                            is_continuous = False
                            break
                    except (TypeError, ValueError):
                        is_continuous = False
                        break
                
                if pt < 1:
                    L_right = sympy.limit(f, x, pt, dir='+')
                    try:
                        if abs(float(L_right) - v_float) > 1e-7:
                            is_continuous = False
                            break
                    except (TypeError, ValueError):
                        is_continuous = False
                        break
        h1_ok = is_continuous
    except Exception:
        h1_ok = False

    # neg_Q: The sequence of polynomials B_n(f) does NOT converge uniformly to f on 0 to 1
    neg_q_ok = False
    try:
        f = witness
        def eval_B(n, f_expr, pt):
            res = 0.0
            for i in range(n + 1):
                val = float(f_expr.subs(x, sympy.Rational(i, n)))
                term = val * math.comb(n, i) * (pt ** i) * ((1.0 - pt) ** (n - i))
                res += term
            return res

        sups = []
        for n in [10, 20, 40]:
            max_diff = 0.0
            for i in range(101):
                pt = i / 100.0
                f_val = float(f.subs(x, pt))
                bn_val = eval_B(n, f, pt)
                d = abs(bn_val - f_val)
                if d > max_diff:
                    max_diff = d
            sups.append(max_diff)
        
        if len(sups) == 3:
            if sups[2] > 0.05 and sups[2] >= sups[1] * 0.8:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous real-valued function on the closed interval 0 to 1",
    "¬Q: The sequence of polynomials B_n(f) does NOT converge uniformly to f on 0 to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1