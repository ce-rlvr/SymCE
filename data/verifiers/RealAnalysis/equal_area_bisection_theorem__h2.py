import sympy
from sympy import Symbol, Interval, integrate, solveset, EmptySet
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)
c = Symbol('c', real=True)

def conditions(witness) -> list[bool]:
    try:
        f = sympy.sympify(witness[0])
        a = sympy.sympify(witness[1])
        b = sympy.sympify(witness[2])
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        if float(a) < float(b):
            domain = continuous_domain(f, x, Interval(a, b))
            if domain == Interval(a, b):
                h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        g = integrate(f, (x, a, c)) - integrate(f, (x, c, b))
        roots = solveset(g, c, domain=Interval.open(a, b))
        if roots == EmptySet or getattr(roots, 'is_empty', False) is True:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is continuous on interval a to b",
    "¬Q: no c in interval a to b bisects the area"
]

N_HYP = 1
NEG_Q_INDEX = 1