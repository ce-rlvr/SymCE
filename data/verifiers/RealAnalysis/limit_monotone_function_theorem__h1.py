import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, a, b, c) where f is a SymPy expression or callable.
    """
    try:
        f, a, b, c = witness
    except Exception:
        return [False, False, False]
        
    if isinstance(f, sp.Expr):
        f_expr = f
        symbols = f.free_symbols
        var = list(symbols)[0] if len(symbols) == 1 else x
    else:
        try:
            f_expr = f(x)
            var = x
        except Exception:
            return [False, False, False]

    # H1: f is monotonically increasing on (a, b)
    h1_ok = False
    try:
        a_val = float(a) if a != -sp.oo else -1000.0
        b_val = float(b) if b != sp.oo else 1000.0
        
        if b_val <= a_val:
            h1_ok = True
        else:
            margin = min(1e-5, (b_val - a_val) / 100.0)
            num_pts = 500
            step = (b_val - margin - (a_val + margin)) / (num_pts - 1)
            pts = [a_val + margin + i * step for i in range(num_pts)]
            
            try:
                c_val = float(c)
                if a_val < c_val < b_val:
                    pts.append(c_val)
                    c_margin = min(1e-5, (c_val - a_val) / 2.0, (b_val - c_val) / 2.0)
                    pts.append(c_val - c_margin)
                    pts.append(c_val + c_margin)
            except Exception:
                pass
            pts.sort()
            
            try:
                f_lam = sp.lambdify(var, f_expr, modules=['math'])
                vals = []
                for p in pts:
                    try:
                        vals.append(float(f_lam(p)))
                    except Exception:
                        vals.append(float('nan'))
            except Exception:
                vals = []
                for p in pts:
                    try:
                        vals.append(float(f_expr.subs(var, p)))
                    except Exception:
                        vals.append(float('nan'))
                        
            valid_vals = [v for v in vals if not math.isnan(v)]
            
            h1_ok = True
            for i in range(len(valid_vals)-1):
                if valid_vals[i] > valid_vals[i+1] + 1e-7:
                    h1_ok = False
                    break
            if len(valid_vals) < 2:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H2: c is a point in (a, b)
    h2_ok = False
    try:
        if float(a) < float(c) < float(b):
            h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion fails
    # Conclusion: limits exist in R, and lim_left <= f(c) <= lim_right
    neg_q = False
    try:
        lim_left = sp.limit(f_expr, var, c, dir='-')
        lim_right = sp.limit(f_expr, var, c, dir='+')
        
        def is_finite_real(val):
            if val is None: return False
            try:
                fval = float(val)
                return not math.isnan(fval) and not math.isinf(fval)
            except Exception:
                return False

        if is_finite_real(lim_left) and is_finite_real(lim_right):
            fc = f_expr.subs(var, c)
            if is_finite_real(fc):
                if float(lim_left) <= float(fc) + 1e-9 and float(fc) <= float(lim_right) + 1e-9:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is monotonically increasing on (a, b)",
    "H_2: c is a point in (a, b)",
    "¬Q: The one-sided limits do not exist in R, or the inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2