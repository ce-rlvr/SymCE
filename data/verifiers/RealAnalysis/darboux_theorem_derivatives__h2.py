import sympy
from sympy import Symbol, Interval, solveset, S
from sympy.calculus.util import continuous_domain
import sympy.abc

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide a function f(x), interval endpoints a and b, and a target derivative y.
    It can be a dictionary {'f': expr, 'a': val, 'b': val, 'y': val} or a tuple (f, a, b, y).
    """
    try:
        if isinstance(witness, dict):
            f_raw = witness.get('f', x)
            a_raw = witness.get('a', 0)
            b_raw = witness.get('b', 1)
            y_raw = witness.get('y', 2)
        else:
            f_raw, a_raw, b_raw, y_raw = witness
            
        f = sympy.sympify(f_raw, locals={'x': x})
        a = sympy.sympify(a_raw)
        b = sympy.sympify(b_raw)
        y = sympy.sympify(y_raw)
    except Exception:
        return [False, False]

    # H_1: f is differentiable on the closed interval
    try:
        if not (a.is_real and b.is_real and bool(a < b)):
            h1 = False
        else:
            df = f.diff(x)
            dom_f = continuous_domain(f, x, Interval(a, b))
            dom_df = continuous_domain(df, x, Interval(a, b))
            h1 = (dom_f == Interval(a, b)) and (dom_df == Interval(a, b))
    except Exception:
        h1 = False

    # ¬Q: There is NO c in the open interval such that f'(c) = y
    try:
        df = f.diff(x)
        sols = solveset(df - y, x, domain=Interval.open(a, b))
        neg_q = (sols == S.EmptySet)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is differentiable on the closed interval",
    "¬Q: There is no c in the open interval such that the derivative is y"
]

N_HYP = 1
NEG_Q_INDEX = 1