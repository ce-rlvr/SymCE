import sympy as sp

# Top-level setup for named objects that the witness expression may reference
x, y = sp.symbols('x y', positive=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, q, f, g) where:
      - p, q are real numbers > 1
      - f is a sympy expression in x (or a callable)
      - g is a sympy expression in y (or a callable)
    """
    try:
        p, q, f, g = witness
    except Exception:
        return [False, False, False]
        
    # Safely convert f and g to sympy expressions
    if callable(f):
        try:
            f_expr = sp.sympify(f(x))
        except Exception:
            f_expr = sp.sympify(f)
    else:
        f_expr = sp.sympify(f)
        
    if callable(g):
        try:
            g_expr = sp.sympify(g(y))
        except Exception:
            g_expr = sp.sympify(g)
    else:
        g_expr = sp.sympify(g)

    # H_1: p and q are real numbers strictly greater than 1 such that 1/p + 1/q = 1
    try:
        p_val = float(p)
        q_val = float(q)
        h1 = bool(p_val > 1.0 and q_val > 1.0 and abs((1.0 / p_val) + (1.0 / q_val) - 1.0) < 1e-9)
    except Exception:
        h1 = False
        
    # H_2: f is a non-negative measurable function in L^p(0, \infty)
    try:
        # Check non-negativity by sampling a few points
        f_vals = []
        for val in [0.1, 1.0, 10.0, 100.0]:
            v = float(f_expr.subs(x, val).evalf())
            f_vals.append(v)
        f_nonneg = all(v >= -1e-9 for v in f_vals)
        
        # Check if f is in L^p
        f_norm_p_pow = sp.integrate(sp.Abs(f_expr)**p, (x, 0, sp.oo))
        if f_norm_p_pow == sp.oo or f_norm_p_pow.has(sp.nan) or f_norm_p_pow.has(sp.zoo):
            f_in_Lp = False
        else:
            f_in_Lp = bool(float(f_norm_p_pow.evalf()) >= 0)
            
        h2 = bool(f_nonneg and f_in_Lp)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: \int_0^\infty \int_0^\infty \frac{f(x)g(y)}{x+y} dx dy \le \frac{\pi}{\sin(\pi/p)} \|f\|_p \|g\|_q
    try:
        LHS = sp.integrate(f_expr * g_expr / (x + y), (x, 0, sp.oo), (y, 0, sp.oo))
        
        # Recompute f_norm just in case
        f_norm_p_pow = sp.integrate(sp.Abs(f_expr)**p, (x, 0, sp.oo))
        if f_norm_p_pow == sp.oo:
            f_norm = sp.oo
        else:
            f_norm = f_norm_p_pow**(1/p)
            
        g_norm_q_pow = sp.integrate(sp.Abs(g_expr)**q, (y, 0, sp.oo))
        if g_norm_q_pow == sp.oo:
            g_norm = sp.oo
        else:
            g_norm = g_norm_q_pow**(1/q)
            
        RHS = (sp.pi / sp.sin(sp.pi / p)) * f_norm * g_norm
        
        # The conclusion fails if LHS > RHS, or if the inequality is undefined (e.g., NaN)
        if LHS.has(sp.nan) or RHS.has(sp.nan) or LHS.has(sp.zoo) or RHS.has(sp.zoo):
            neg_Q = True
        elif LHS == sp.oo and RHS == sp.oo:
            neg_Q = False
        elif LHS == sp.oo and RHS != sp.oo:
            neg_Q = True
        elif LHS != sp.oo and RHS == sp.oo:
            neg_Q = False
        else:
            lhs_val = float(LHS.evalf())
            rhs_val = float(RHS.evalf())
            # neg_Q is True if LHS is strictly greater than RHS (allowing for small float inaccuracies)
            neg_Q = not (lhs_val <= rhs_val + 1e-9)
    except Exception:
        neg_Q = False
        
    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: p and q are real numbers strictly greater than 1 such that 1/p + 1/q = 1",
    "H_2: f is a non-negative measurable function in L^p(0, oo)",
    "¬Q: The inequality fails (LHS > RHS or undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2