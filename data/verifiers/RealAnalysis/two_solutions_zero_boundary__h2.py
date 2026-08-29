import sympy
from sympy import Symbol, Interval, solveset, S
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f_expr = sympy.sympify(witness['f'])
        a = sympy.sympify(witness['a'])
        b = sympy.sympify(witness['b'])
        x0 = sympy.sympify(witness['x0'])
        k = sympy.sympify(witness['k'])
        
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            orig_sym = list(free_syms)[0]
            f_expr = f_expr.subs(orig_sym, x)
        
        sym = x
    except Exception:
        return [False, False, False, False]

    # H1: f is a continuous real-valued function on the closed interval
    try:
        if not (a.is_real and b.is_real and bool(a < b)):
            h1 = False
        else:
            domain = continuous_domain(f_expr, sym, Interval(a, b))
            h1 = (domain == Interval(a, b))
    except Exception:
        h1 = False

    # H2: There exists a point x_0 in the open interval such that f(x_0) > 0
    try:
        if not x0.is_real:
            h2 = False
        else:
            f_x0 = f_expr.subs(sym, x0)
            h2 = bool(a < x0) and bool(x0 < b) and bool(f_x0 > 0)
    except Exception:
        h2 = False

    # H3: k is a real number such that 0 < k < f(x_0)
    try:
        if not k.is_real:
            h3 = False
        else:
            f_x0 = f_expr.subs(sym, x0)
            h3 = bool(0 < k) and bool(k < f_x0)
    except Exception:
        h3 = False

    # ¬Q: There do NOT exist at least two distinct points c_1, c_2 such that f(c_1) = f(c_2) = k
    try:
        sols = solveset(f_expr - k, sym, domain=Interval.open(a, b))
        if sols == S.EmptySet:
            neg_q = True
        elif isinstance(sols, sympy.FiniteSet):
            neg_q = len(sols) < 2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous real-valued function on the closed interval",
    "H_2: There exists a point x_0 in the open interval such that f(x_0) > 0",
    "H_3: k is a real number such that 0 < k < f(x_0)",
    "¬Q: There do not exist at least two distinct points c_1, c_2 such that f(c_1) = f(c_2) = k"
]

N_HYP = 3
NEG_Q_INDEX = 3