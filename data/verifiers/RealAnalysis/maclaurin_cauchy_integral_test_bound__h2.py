import sympy
from sympy import Symbol, Sum, Integral, oo, Lambda

x = Symbol('x', real=True)
k = Symbol('k', integer=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a SymPy expression in terms of x, a Lambda, 
    or a tuple (f, n) where n is the upper bound.
    """
    if isinstance(witness, tuple):
        if len(witness) == 2:
            f_input, n_val = witness
        else:
            return [False, False, False, False]
    else:
        f_input = witness
        n_val = oo  # Default to oo to catch divergence counterexamples

    try:
        if callable(f_input) or isinstance(f_input, Lambda):
            f_expr = f_input(x)
        else:
            f_expr = sympy.sympify(f_input)
    except Exception:
        return [False, False, False, False]

    # H1: f is a non-negative real-valued function on [1, oo)
    try:
        pts = [1, 1.5, 2, 2.5, 3, 10, 100]
        h1_ok = all(float(f_expr.subs(x, p).evalf()) >= -1e-9 for p in pts)
    except Exception:
        h1_ok = False

    # H2: f is continuous on [1, oo)
    try:
        pts = [1.1, 1.5, 2.1, 2.5, 3.14, 10.5]
        h2_ok = True
        for p in pts:
            val = f_expr.subs(x, p).evalf()
            if not val.is_real or val.has(sympy.nan) or val.has(sympy.zoo):
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # H3: f is monotonically decreasing on [1, oo)
    try:
        pts = [1, 1.5, 2, 2.5, 3, 10, 100]
        vals = [float(f_expr.subs(x, p).evalf()) for p in pts]
        h3_ok = all(vals[i] >= vals[i+1] - 1e-9 for i in range(len(vals)-1))
        
        # Also check derivative at a few points to be robust
        if h3_ok:
            df = sympy.diff(f_expr, x)
            df_vals = [float(df.subs(x, p).evalf()) for p in [1.2, 2.2, 5.5, 50.1]]
            if any(v > 1e-9 for v in df_vals):
                h3_ok = False
    except Exception:
        h3_ok = False

    # Conclusion: 0 <= Sum(f(k), (k, 1, n)) - Integral(f(x), (x, 1, n)) <= f(1)
    try:
        # If n_val is a symbol, evaluate at a specific integer to avoid false positives
        if isinstance(n_val, sympy.Symbol):
            test_n = 10
        else:
            test_n = n_val
            
        sum_val = Sum(f_expr.subs(x, k), (k, 1, test_n)).doit()
        int_val = Integral(f_expr, (x, 1, test_n)).doit()
        
        diff_val = sum_val - int_val
        f1_val = f_expr.subs(x, 1).doit()
        
        diff_num = diff_val.evalf()
        f1_num = f1_val.evalf()
        
        # If the difference evaluates to nan (e.g., oo - oo), the inequalities fail.
        if diff_num.has(sympy.nan) or diff_num.has(sympy.zoo) or diff_num.has(oo) or diff_num.has(-oo):
            q_ok = False
        else:
            try:
                lower_ok = bool(diff_num >= -1e-9)
                upper_ok = bool(diff_num <= f1_num + 1e-9)
                q_ok = lower_ok and upper_ok
            except TypeError:
                q_ok = False
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-negative real-valued function on [1, oo)",
    "H_2: f is continuous on [1, oo)",
    "H_3: f is monotonically decreasing on [1, oo)",
    "¬Q: The bound 0 <= Sum - Integral <= f(1) fails (e.g., evaluates to undefined/nan for n=oo)"
]

N_HYP = 3
NEG_Q_INDEX = 3