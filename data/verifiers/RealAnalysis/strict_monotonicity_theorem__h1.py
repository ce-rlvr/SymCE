import sympy
from sympy import Symbol

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f, a, b = witness
    except Exception:
        return [False, False, False]
    
    try:
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
    except Exception:
        return [False, False, False]

    try:
        a_val = float(a)
        b_val = float(b)
        if a_val >= b_val:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    N = 100
    points = [a_val + (b_val - a_val) * i / float(N) for i in range(1, N)]
    
    h1 = True
    h2 = True
    try:
        df = sympy.diff(f_expr, x)
        for p in points:
            val = df.subs(x, p).evalf()
            if val.has(sympy.nan) or val.has(sympy.oo) or val.has(-sympy.oo) or val.has(sympy.zoo):
                h1 = False
                h2 = False
                break
            try:
                val_float = float(val)
            except TypeError:
                try:
                    cval = complex(val)
                    if abs(cval.imag) > 1e-9:
                        h1 = False
                        h2 = False
                        break
                    val_float = cval.real
                except Exception:
                    h1 = False
                    h2 = False
                    break

            if val_float <= 0:
                h2 = False
    except Exception:
        h1 = False
        h2 = False

    neg_q = False
    try:
        fa = f_expr.subs(x, a_val).evalf()
        fb = f_expr.subs(x, b_val).evalf()
        
        def is_valid_real(v):
            if v.has(sympy.nan) or v.has(sympy.oo) or v.has(-sympy.oo) or v.has(sympy.zoo):
                return False, 0.0
            try:
                return True, float(v)
            except TypeError:
                try:
                    cval = complex(v)
                    if abs(cval.imag) > 1e-9:
                        return False, 0.0
                    return True, cval.real
                except Exception:
                    return False, 0.0

        valid_a, fa_float = is_valid_real(fa)
        valid_b, fb_float = is_valid_real(fb)

        if not valid_a or not valid_b:
            neg_q = True
        else:
            if fa_float >= fb_float:
                neg_q = True
            else:
                for p in points:
                    fp = f_expr.subs(x, p).evalf()
                    valid_p, fp_float = is_valid_real(fp)
                    if not valid_p:
                        neg_q = True
                        break
                    if fa_float >= fp_float or fp_float >= fb_float:
                        neg_q = True
                        break
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is differentiable on (a, b)",
    "H_2: forall x in (a, b), f'(x) > 0",
    "¬Q: f is not strictly monotonically increasing on the closed interval a to b"
]

N_HYP = 2
NEG_Q_INDEX = 2