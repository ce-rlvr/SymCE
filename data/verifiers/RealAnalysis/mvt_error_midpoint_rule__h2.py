import sympy as sp
from sympy import Symbol, diff, integrate, solveset, Eq, Interval, S
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f_expr, a_val, b_val = witness
        f = sp.sympify(f_expr)
        a = sp.sympify(a_val)
        b = sp.sympify(b_val)
        
        if isinstance(a, sp.Float):
            a = sp.nsimplify(a, rational=True)
        if isinstance(b, sp.Float):
            b = sp.nsimplify(b, rational=True)
            
    except Exception:
        return [False, False]

    free_symbols = f.free_symbols
    if len(free_symbols) > 1:
        return [False, False]
    elif len(free_symbols) == 1:
        var = list(free_symbols)[0]
    else:
        var = Symbol('x', real=True)

    try:
        if not a.is_real or not b.is_real:
            h1 = False
        elif a >= b:
            h1 = False
        else:
            f1 = diff(f, var)
            f2 = diff(f1, var)
            domain = continuous_domain(f2, var, S.Reals)
            h1 = bool(Interval(a, b).is_subset(domain))
    except Exception:
        h1 = False

    try:
        c_sym = Symbol('c_dummy', real=True)
        lhs = integrate(f, (var, a, b)) - (b - a) * f.subs(var, (a + b) / 2)
        rhs_c = ((b - a)**3 / 24) * f2.subs(var, c_sym)
        
        if a >= b:
            neg_q = True
        else:
            sol = solveset(Eq(rhs_c, lhs), c_sym, domain=Interval.open(a, b))
            if sol == S.EmptySet:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is twice continuously differentiable on the interval",
    "not Q: There does not exist c in the interval satisfying the midpoint rule error formula"
]

N_HYP = 1
NEG_Q_INDEX = 1