import sympy
from sympy import Symbol, Interval, pi, diff, simplify
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    h1_ok = False
    try:
        domain = Interval(-pi, pi)
        if continuous_domain(witness, x, domain) == domain:
            df = diff(witness, x)
            if continuous_domain(df, x, domain) == domain:
                h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        diff_val = simplify(witness.subs(x, -pi) - witness.subs(x, pi))
        if diff_val != 0:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable real-valued function on the interval from minus pi to pi",
    "¬Q: The Fourier series of f does not converge uniformly to f on the interval from minus pi to pi"
]

N_HYP = 1
NEG_Q_INDEX = 1