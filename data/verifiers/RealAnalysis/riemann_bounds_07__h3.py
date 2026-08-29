import sympy
from sympy import Symbol, Abs, integrate

# Top-level setup
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f and g are Riemann integrable",
    "H_2: p > 1 and q > 1",
    "not Q: Integral of |f g| > (Integral of |f|^p)^(1/p) (Integral of |g|^q)^(1/q)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
            a = witness['a']
            b = witness['b']
            p = witness['p']
            q = witness['q']
        else:
            f, g, a, b, p, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: f and g are Riemann integrable
    try:
        a_sym = sympy.sympify(a, locals={'x': x})
        b_sym = sympy.sympify(b, locals={'x': x})
        f_sym = sympy.sympify(f, locals={'x': x})
        g_sym = sympy.sympify(g, locals={'x': x})
        
        if a_sym.is_real is not True or b_sym.is_real is not True:
            h1 = False
        elif bool(a_sym < b_sym) is not True:
            h1 = False
        else:
            # Basic sanity check for integrability: no singularities at the midpoint
            mid = (a_sym + b_sym) / 2
            f_mid = f_sym.subs(x, mid)
            g_mid = g_sym.subs(x, mid)
            if f_mid.has(sympy.oo, sympy.zoo, sympy.nan) or g_mid.has(sympy.oo, sympy.zoo, sympy.nan):
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H_2: p > 1 and q > 1
    try:
        p_sym = sympy.sympify(p, locals={'x': x})
        q_sym = sympy.sympify(q, locals={'x': x})
        if p_sym.is_real is not True or q_sym.is_real is not True:
            h2 = False
        else:
            h2 = bool(p_sym > 1 and q_sym > 1)
    except Exception:
        h2 = False

    # ¬Q: Integral |f(x)g(x)| dx > (Integral |f(x)|^p dx)^{1/p} (Integral |g(x)|^q dx)^{1/q}
    try:
        LHS_expr = integrate(Abs(f_sym * g_sym), (x, a_sym, b_sym))
        int_fp = integrate(Abs(f_sym)**p_sym, (x, a_sym, b_sym))
        int_gq = integrate(Abs(g_sym)**q_sym, (x, a_sym, b_sym))
        
        RHS_expr = (int_fp)**(sympy.S(1)/p_sym) * (int_gq)**(sympy.S(1)/q_sym)
        
        LHS_val = LHS_expr.evalf()
        RHS_val = RHS_expr.evalf()
        
        lhs_float = float(LHS_val)
        rhs_float = float(RHS_val)
        
        # Strict inequality for the negated conclusion
        neg_q = lhs_float > rhs_float + 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]