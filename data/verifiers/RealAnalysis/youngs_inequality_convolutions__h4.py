import sympy as sp

x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)

def get_norm(expr, var, p):
    if p == sp.oo:
        if expr.is_constant(var):
            return sp.Abs(expr)
        return sp.oo
    else:
        integrand = sp.Abs(expr)**p
        integral = sp.integrate(integrand, (var, -sp.oo, sp.oo))
        if integral == sp.oo:
            return sp.oo
        if integral.has(sp.Integral):
            # Fallback: try without Abs in case SymPy couldn't simplify it
            integral_no_abs = sp.integrate(expr**p, (var, -sp.oo, sp.oo))
            if not integral_no_abs.has(sp.Integral):
                return integral_no_abs**(1/p)
            raise ValueError("Could not compute integral")
        return integral**(1/p)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false Young's Inequality conjecture.
    Expected witness dictionary:
    {
        'p': value,
        'q': value,
        'r': value,
        'f': sympy expression in terms of var,
        'g': sympy expression in terms of var,
        'x': sympy symbol used in f and g
    }
    """
    try:
        p = witness['p']
        q = witness['q']
        r = witness['r']
        f = witness['f']
        g = witness['g']
        var = witness['x']
    except (KeyError, TypeError):
        return [False, False, False, False]

    # H_1: 1 <= p, q, r <= infinity
    try:
        def is_valid(val):
            if val == sp.oo:
                return True
            return bool(val >= 1)
        h1 = is_valid(p) and is_valid(q) and is_valid(r)
    except Exception:
        h1 = False

    # H_2: 1/p + 1/q = 1 + 1/r
    try:
        def inv(val):
            return 0 if val == sp.oo else 1/sp.S(val)
        left = inv(p) + inv(q)
        right = 1 + inv(r)
        h2 = bool(sp.Eq(left, right))
    except Exception:
        h2 = False

    # H_3: f \in L^p(R^n)
    norm_f = None
    try:
        norm_f = get_norm(f, var, p)
        h3 = bool(norm_f < sp.oo)
    except Exception:
        h3 = False

    # neg_Q: f * g \notin L^r(R^n) or ||f * g||_r > ||f||_p ||g||_q
    try:
        y_sym = sp.Symbol('y', real=True)
        integrand = f.subs(var, y_sym - var) * g
        conv = sp.integrate(integrand, (var, -sp.oo, sp.oo))
        
        if conv.has(sp.Integral):
            neg_q = False
        else:
            norm_conv = get_norm(conv, y_sym, r)
            if norm_conv == sp.oo:
                neg_q = True
            else:
                if norm_f is None:
                    norm_f = get_norm(f, var, p)
                norm_g = get_norm(g, var, q)
                
                if norm_f * norm_g == sp.oo:
                    neg_q = False
                else:
                    neg_q = bool(norm_conv > norm_f * norm_g)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: 1 <= p, q, r <= infinity",
    "H_2: 1/p + 1/q = 1 + 1/r",
    "H_3: f is in L^p(R^n)",
    "¬Q: f * g is not in L^r(R^n) or ||f * g||_r > ||f||_p ||g||_q"
]

N_HYP = 3
NEG_Q_INDEX = 3