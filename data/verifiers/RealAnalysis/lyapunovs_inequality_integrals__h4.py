import sympy
from sympy import Symbol, diff, integrate, Abs, simplify, Interval, S
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            q = witness.get('q')
            y = witness.get('y')
        else:
            a, b, q, y = witness
            
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        q_expr = sympy.sympify(q)
        y_expr = sympy.sympify(y)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = False
        if bool(a < b):
            domain_q = continuous_domain(q_expr, x, S.Reals)
            if Interval(a, b).is_subset(domain_q):
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        y_diff2 = diff(y_expr, x, 2)
        domain_y2 = continuous_domain(y_diff2, x, S.Reals)
        if Interval(a, b).is_subset(domain_y2):
            eq = simplify(y_diff2 + q_expr * y_expr)
            if eq == 0:
                h2 = True
    except Exception:
        h2 = False

    try:
        h3 = False
        if simplify(y_expr.subs(x, a)) == 0 and simplify(y_expr.subs(x, b)) == 0:
            h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        integral_val = integrate(Abs(q_expr), (x, a, b))
        if float(integral_val.evalf()) <= 4.0 / float((b - a).evalf()):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: q is a continuous real-valued function on the interval a to b",
    "H_2: There exists a twice continuously differentiable real-valued function y such that y_double_prime + q y = 0",
    "H_3: y(a) = 0 and y(b) = 0",
    "not Q: integral of abs(q(x)) from a to b <= 4 / (b - a)"
]

N_HYP = 3
NEG_Q_INDEX = 3