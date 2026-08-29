import sympy
from sympy.abc import x
from sympy import Piecewise, Interval, solveset, S, sympify

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a dictionary with keys 'f', 'g', 'a', 'b' or a tuple (f, g, a, b).
    f and g can be sympy expressions (in terms of x), strings, or callable python functions.
    a and b should be real numbers.
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, g, a, b = witness
    except Exception:
        return [False, False, False]

    try:
        if not callable(f):
            f = sympify(f)
        if not callable(g):
            g = sympify(g)
        a = sympify(a)
        b = sympify(b)
    except Exception:
        pass

    # H_1: f(a) < g(a)
    try:
        fa = f(a) if callable(f) else f.subs(x, a)
        ga = g(a) if callable(g) else g.subs(x, a)
        h1 = bool(fa < ga)
    except Exception:
        h1 = False

    # H_2: f(b) > g(b)
    try:
        fb = f(b) if callable(f) else f.subs(x, b)
        gb = g(b) if callable(g) else g.subs(x, b)
        h2 = bool(fb > gb)
    except Exception:
        h2 = False

    # ¬Q: There does not exist c in (a, b) such that f(c) = g(c)
    neg_q = False
    try:
        if callable(f) or callable(g):
            # We cannot reliably prove non-intersection for arbitrary python functions
            # within the constraints, so we default to False.
            pass
        else:
            domain = Interval.open(a, b)
            sols = solveset(f - g, x, domain=domain)
            if sols is S.EmptySet:
                neg_q = True
            elif sols.is_empty == False:
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(a) < g(a)",
    "H_2: f(b) > g(b)",
    "¬Q: There does not exist c in (a, b) such that f(c) = g(c)"
]

N_HYP = 2
NEG_Q_INDEX = 2