import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy import Interval, S
from sympy.abc import x

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the function f, the interval bounds a and b,
    and the values M and m (which were unconstrained due to a dropped hypothesis).
    """
    try:
        if isinstance(witness, dict):
            f_expr = witness['f']
            a = witness['a']
            b = witness['b']
            M = witness['M']
            m = witness['m']
        elif hasattr(witness, 'f'):
            f_expr = witness.f
            a = witness.a
            b = witness.b
            M = witness.M
            m = witness.m
        else:
            f_expr, a, b, M, m = witness
    except Exception:
        return [False, False, False]
        
    try:
        f_expr = sp.sympify(f_expr)
        free_vars = f_expr.free_symbols
        if len(free_vars) > 1:
            return [False, False, False]
        elif len(free_vars) == 1:
            var = list(free_vars)[0]
        else:
            var = x
    except Exception:
        return [False, False, False]
        
    try:
        a = sp.sympify(a)
        b = sp.sympify(b)
        M = sp.sympify(M)
        m = sp.sympify(m)
    except Exception:
        return [False, False, False]

    # H_1: f is a continuous real-valued function on the closed interval a to b
    try:
        if not bool(a < b):
            h1 = False
        else:
            domain = continuous_domain(f_expr, var, S.Reals)
            h1 = bool(Interval(a, b).is_subset(domain))
    except Exception:
        h1 = False
        
    # H_2: integral of f(x) from a to b is 0
    try:
        int_f = sp.integrate(f_expr, (var, a, b))
        h2 = bool(sp.simplify(int_f) == 0)
    except Exception:
        h2 = False
        
    # ¬Q: |integral of x*f(x) from a to b| > (b-a)^2 / 8 * (M - m)
    try:
        int_xf = sp.integrate(var * f_expr, (var, a, b))
        lhs = sp.Abs(int_xf)
        rhs = sp.Rational(1, 8) * (b - a)**2 * (M - m)
        diff = sp.simplify(lhs - rhs)
        try:
            neg_q = bool(diff > 0)
        except TypeError:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous real-valued function on the closed interval a to b",
    "H_2: integral of f(x) from a to b is 0",
    "not Q: absolute value of integral of x f(x) from a to b > (b-a)^2 / 8 * (M - m)"
]

N_HYP = 2
NEG_Q_INDEX = 2