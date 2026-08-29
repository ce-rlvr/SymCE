import sympy
from sympy import integrate, Sum, Abs, oo, Symbol, S

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True)

def get_norm(expr, p, space, domain):
    try:
        if space == 'R':
            if p == oo:
                from sympy.calculus.util import maximum
                res = maximum(Abs(expr), x, sympy.Interval(domain[0], domain[1]))
                return res
            else:
                integrand = Abs(expr)**p
                res = integrate(integrand, (x, domain[0], domain[1]))
                if hasattr(res, 'has') and res.has(sympy.Integral):
                    res = res.evalf()
                if res == oo or res == sympy.zoo or str(res) == 'nan':
                    return oo
                try:
                    if float(res) < 0:
                        res = S(0)
                except Exception:
                    pass
                return res**(1/p)
        elif space == 'N':
            if p == oo:
                y = Symbol('y', real=True)
                expr_y = expr.subs(n, y)
                from sympy.calculus.util import maximum
                res = maximum(Abs(expr_y), y, sympy.Interval(domain[0], domain[1]))
                return res
            else:
                integrand = Abs(expr)**p
                res = Sum(integrand, (n, domain[0], domain[1])).doit()
                if hasattr(res, 'has') and res.has(Sum):
                    res = res.evalf()
                if res == oo or res == sympy.zoo or str(res) == 'nan':
                    return oo
                try:
                    if float(res) < 0:
                        res = S(0)
                except Exception:
                    pass
                return res**(1/p)
    except Exception:
        return None

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for Hölder's Inequality.
    The witness is expected to be a dictionary with keys:
      - 'space': 'R' (for integrals over reals) or 'N' (for sums over integers)
      - 'domain': tuple of (lower_bound, upper_bound)
      - 'p': value for p (number or sympy.oo)
      - 'q': value for q (number or sympy.oo)
      - 'f': sympy expression in terms of x (if 'R') or n (if 'N')
      - 'g': sympy expression in terms of x (if 'R') or n (if 'N')
    """
    # H1: (X, \Sigma, \mu) is a measure space
    try:
        space = witness.get('space')
        domain = witness.get('domain')
        h1 = space in ['R', 'N'] and isinstance(domain, (tuple, list)) and len(domain) == 2
    except Exception:
        h1 = False

    # H2: 1 \le p, q \le \infty
    try:
        p = witness.get('p')
        q = witness.get('q')
        h2 = (1 <= p) and (1 <= q)
    except Exception:
        h2 = False

    # H3: \frac{1}{p} + \frac{1}{q} = 1
    try:
        if p == oo and q == 1:
            h3 = True
        elif q == oo and p == 1:
            h3 = True
        elif p == oo or q == oo:
            h3 = False
        else:
            val = 1/p + 1/q
            h3 = abs(float(val) - 1.0) < 1e-9
    except Exception:
        h3 = False

    # H4: f \in L^p(X, \mu)
    try:
        f = witness.get('f')
        norm_f = get_norm(f, p, space, domain)
        h4 = (norm_f is not None) and (norm_f < oo)
    except Exception:
        h4 = False

    # Negated Conclusion: fg is NOT in L^1(X, \mu) OR \|fg\|_1 > \|f\|_p \|g\|_q
    try:
        g = witness.get('g')
        norm_fg = get_norm(f * g, 1, space, domain)
        norm_g = get_norm(g, q, space, domain)
        
        if norm_fg is None or norm_g is None or norm_f is None:
            neg_q = False
        elif norm_fg == oo:
            neg_q = True
        else:
            if norm_g == oo:
                neg_q = False
            else:
                diff = norm_fg - norm_f * norm_g
                neg_q = bool(diff.evalf() > 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: (X, Sigma, mu) is a measure space",
    "H_2: 1 <= p, q <= infinity",
    "H_3: 1/p + 1/q = 1",
    "H_4: f is in L^p(X, mu)",
    "¬Q: fg is not in L^1(X, mu) or ||fg||_1 > ||f||_p ||g||_q"
]

N_HYP = 4
NEG_Q_INDEX = 4