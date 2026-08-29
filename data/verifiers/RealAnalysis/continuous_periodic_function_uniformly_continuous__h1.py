import sympy
from sympy.abc import x
import math

def conditions(witness) -> list[bool]:
    try:
        witness = sympy.sympify(witness)
    except Exception:
        pass

    h1_ok = False
    neg_q_ok = False

    # H_1: There exists P > 0 such that f(x + P) = f(x) for all x \in \mathbb{R}
    try:
        p = None
        if hasattr(sympy, 'periodicity'):
            p = sympy.periodicity(witness, x)
            
        if p is not None and p > 0:
            h1_ok = True
        else:
            for p_val in [1, 2, sympy.pi, 2*sympy.pi, sympy.Rational(1, 2)]:
                try:
                    diff = sympy.simplify(witness.subs(x, x + p_val) - witness)
                    if diff == 0:
                        h1_ok = True
                        break
                    val1 = abs(float(diff.subs(x, 0.12345).evalf()))
                    val2 = abs(float(diff.subs(x, 0.54321).evalf()))
                    val3 = abs(float(diff.subs(x, -0.76543).evalf()))
                    val4 = abs(float(diff.subs(x, -1.23456).evalf()))
                    if max(val1, val2, val3, val4) < 1e-9:
                        h1_ok = True
                        break
                except Exception:
                    pass
            
            if not h1_ok:
                try:
                    if sympy.simplify(sympy.diff(witness, x)) == 0:
                        h1_ok = True
                except Exception:
                    pass
    except Exception:
        h1_ok = False

    # neg_Q: f is not uniformly continuous on \mathbb{R}
    try:
        def check_jump(x0, x1, depth=0):
            if depth > 3:
                return True
            try:
                sub_points = [x0 + j*(x1-x0)/10.0 for j in range(11)]
                sub_vals = []
                for p in sub_points:
                    val = witness.subs(x, p).evalf()
                    if not val.is_real:
                        return True
                    sub_vals.append(float(val))
                
                for j in range(10):
                    if abs(sub_vals[j+1] - sub_vals[j]) > 0.4:
                        if check_jump(sub_points[j], sub_points[j+1], depth+1):
                            return True
                return False
            except Exception:
                return True

        points = [i/100.0 for i in range(-300, 300)]
        for i in range(len(points)-1):
            x0 = points[i]
            x1 = points[i+1]
            try:
                v0 = witness.subs(x, x0).evalf()
                v1 = witness.subs(x, x1).evalf()
                if not v0.is_real or not v1.is_real:
                    neg_q_ok = True
                    break
                if abs(float(v1) - float(v0)) > 0.4:
                    if check_jump(x0, x1, 0):
                        neg_q_ok = True
                        break
            except Exception:
                neg_q_ok = True
                break
        
        if not neg_q_ok:
            try:
                df = sympy.diff(witness, x)
                large_points = [10**i for i in range(2, 6)] + [-10**i for i in range(2, 6)]
                for p in large_points:
                    df_val = abs(float(df.subs(x, p).evalf()))
                    if df_val > 1000:
                        df_val2 = abs(float(df.subs(x, p*2).evalf()))
                        if df_val2 > df_val:
                            neg_q_ok = True
                            break
            except Exception:
                pass
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists P > 0 such that f(x + P) = f(x) for all x in R",
    "¬Q: f is not uniformly continuous on R"
]

N_HYP = 1
NEG_Q_INDEX = 1