import sympy
from sympy import Symbol, Set, simplify, Abs, limit, oo, S, Piecewise, Eq, Interval, Limit
from sympy.calculus.util import maximum

# Top-level setup for witness expressions
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    Expected witness format: (f_n_expr, f_expr, x_n_expr, x_val, domain)
    where:
      - f_n_expr: sympy expression for f_n(var)
      - f_expr: sympy expression for f(var)
      - x_n_expr: sympy expression for x_n
      - x_val: sympy value for x
      - domain: sympy Set representing the metric space X
    """
    try:
        f_n_expr, f_expr, x_n_expr, x_val, domain = witness
    except Exception:
        return [False, False, False, False]
        
    # Determine the spatial variable used in the functions
    try:
        spatial_symbols = (f_n_expr.free_symbols | f_expr.free_symbols) - {n}
        if len(spatial_symbols) == 1:
            var = list(spatial_symbols)[0]
        elif len(spatial_symbols) == 0:
            var = y
        else:
            if y in spatial_symbols:
                var = y
            elif x in spatial_symbols:
                var = x
            elif z in spatial_symbols:
                var = z
            else:
                var = list(spatial_symbols)[0]
    except Exception:
        var = y

    # H_1: X is a metric space
    try:
        h1 = isinstance(domain, Set)
    except Exception:
        h1 = False
        
    # H_2: (f_n) converges uniformly to f on X
    try:
        diff = simplify(f_n_expr - f_expr)
        if diff == 0:
            h2 = True
        else:
            sup = maximum(Abs(diff), var, domain)
            lim = limit(sup, n, oo)
            if isinstance(lim, Limit):
                h2 = False
            else:
                h2 = (lim == 0)
    except Exception:
        h2 = False
        
    # H_3: (x_n) is a sequence in X that converges to x in X
    try:
        x_in_domain = domain.contains(x_val)
        if x_in_domain is None:
            x_in_domain = True
        else:
            x_in_domain = bool(x_in_domain)
            
        x_n_in_domain = True
        for i in range(1, 6):
            val = x_n_expr.subs(n, i)
            contains_val = domain.contains(val)
            if contains_val is not None and not bool(contains_val):
                x_n_in_domain = False
                break
                
        lim_x_n = limit(x_n_expr, n, oo)
        if isinstance(lim_x_n, Limit):
            h3 = False
        else:
            h3 = x_in_domain and x_n_in_domain and (lim_x_n == x_val)
    except Exception:
        h3 = False
        
    # ¬Q: f_n(x_n) does NOT converge to f(x)
    try:
        fn_xn = simplify(f_n_expr.subs(var, x_n_expr))
        fx = simplify(f_expr.subs(var, x_val))
        lim_fn_xn = limit(fn_xn, n, oo)
        
        if isinstance(lim_fn_xn, Limit):
            neg_q = False
        else:
            diff_lim = simplify(lim_fn_xn - fx)
            neg_q = (diff_lim != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: (f_n) converges uniformly to f on X",
    "H_3: (x_n) is a sequence in X that converges to x in X",
    "¬Q: f_n(x_n) does not converge to f(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3