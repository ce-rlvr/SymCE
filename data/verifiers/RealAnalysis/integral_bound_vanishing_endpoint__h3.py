import sympy
from sympy import Symbol, Interval, integrate, Abs, simplify
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = sympy.sympify(witness['f'])
            a = sympy.sympify(witness['a'])
            b = sympy.sympify(witness['b'])
            M = sympy.sympify(witness['M'])
        else:
            f, a, b, M = [sympy.sympify(w) for w in witness]
            
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = x
        else:
            var = next((s for s in free_syms if s.name == 'x'), list(free_syms)[0])
    except Exception:
        return [False, False, False, False]

    # H1: f is continuously differentiable on interval a to b
    try:
        df = f.diff(var)
        dom = continuous_domain(df, var, Interval(a, b))
        h1 = bool(Interval(a, b).is_subset(dom))
    except Exception:
        h1 = False

    # H2: f(a) == 0
    try:
        val = simplify(f.subs(var, a))
        h2 = bool(val == 0)
    except Exception:
        h2 = False

    # H3: a < b
    try:
        diff_ab = simplify(b - a)
        if diff_ab.is_positive:
            h3 = True
        elif diff_ab.is_positive is False:
            h3 = False
        else:
            h3 = bool(diff_ab.evalf() > 0)
    except Exception:
        h3 = False

    # neg_Q: |int_a^b f(x) dx| > M/2 * (b-a)^2
    try:
        integral_val = integrate(f, (var, a, b))
        lhs = simplify(Abs(integral_val))
        rhs = simplify(M * (b - a)**2 / 2)
        diff_q = simplify(lhs - rhs)
        if diff_q.is_positive:
            neg_q = True
        elif diff_q.is_positive is False:
            neg_q = False
        else:
            neg_q = bool(diff_q.evalf() > 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuously differentiable on interval a to b",
    "H_2: f(a) = 0",
    "H_3: a < b",
    "not Q: absolute value of integral is greater than M/2 * (b-a)^2"
]

N_HYP = 3
NEG_Q_INDEX = 3