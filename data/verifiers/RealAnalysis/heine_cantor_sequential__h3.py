import sympy
from sympy import Symbol, Interval, FiniteSet, Union, Piecewise, S, sympify
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def is_compact(domain):
    if isinstance(domain, Interval):
        return (not domain.left_open) and (not domain.right_open) and domain.inf.is_finite and domain.sup.is_finite
    if isinstance(domain, FiniteSet):
        return all(elem.is_finite for elem in domain)
    if isinstance(domain, Union):
        return all(is_compact(arg) for arg in domain.args)
    return False

def conditions(witness):
    try:
        domain, f_expr = witness
    except Exception:
        return [False, False, False]
        
    if callable(f_expr):
        try:
            f_expr = f_expr(x)
        except Exception:
            pass

    try:
        f_expr = sympify(f_expr)
    except Exception:
        pass

    try:
        free = f_expr.free_symbols
        if len(free) == 1:
            var = list(free)[0]
        else:
            var = x
    except Exception:
        var = x

    # H1: X is a sequentially compact metric space
    try:
        h1 = bool(is_compact(domain))
    except Exception:
        h1 = False

    # H2: Y is a metric space
    # Any real-valued function maps to R (or C), which is a metric space.
    h2 = True

    # neg_Q: f is NOT uniformly continuous on X
    # On a compact domain, uniform continuity is equivalent to continuity.
    # We check if the function fails to be continuous on the entire domain.
    try:
        cont_dom = continuous_domain(f_expr, var, domain)
        try:
            is_sub = domain.is_subset(cont_dom)
        except Exception:
            is_sub = None
            
        if is_sub is True:
            neg_q = False
        elif is_sub is False:
            neg_q = True
        else:
            neg_q = bool(cont_dom != domain)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a sequentially compact metric space",
    "H_2: Y is a metric space",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2