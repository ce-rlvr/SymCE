import sympy
from sympy import Symbol, integrate, Abs
import math

# Top-level setup: named object bindings that the witness expression may reference
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (f, a, b, M)
    where f is a sympy expression in terms of x, a and b are the interval endpoints,
    and M is the positive constant used in the conclusion.
    """
    try:
        f, a, b, M = witness
    except Exception:
        return [False, False, False]

    # H_1: f is a real-valued function defined on the interval
    try:
        h1 = False
        a_f = float(a)
        b_f = float(b)
        if a_f < b_f:
            pts = [a_f + (b_f - a_f) * i / 50.0 for i in range(51)]
            valid = True
            for p in pts:
                try:
                    v = complex(f.subs(x, p).evalf())
                    if math.isnan(v.real) or math.isnan(v.imag) or abs(v.imag) > 1e-9:
                        valid = False
                        break
                except Exception:
                    valid = False
                    break
            if valid:
                h1 = True
    except Exception:
        h1 = False

    # H_2: f is continuously differentiable on the interval
    try:
        h2 = False
        if h1:
            df = f.diff(x)
            a_f = float(a)
            b_f = float(b)
            pts = [a_f + (b_f - a_f) * i / 50.0 for i in range(51)]
            valid = True
            for p in pts:
                try:
                    v = complex(df.subs(x, p).evalf())
                    if math.isnan(v.real) or math.isnan(v.imag) or abs(v.imag) > 1e-9:
                        valid = False
                        break
                except Exception:
                    valid = False
                    break
            if valid:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    try:
        neg_q = False
        M_f = float(M)
        if M_f > 0:
            lhs_exact = Abs(integrate(f, (x, a, b)) - sympy.Rational(1, 2) * (f.subs(x, a) + f.subs(x, b)) * (b - a))
            rhs_exact = M * (b - a)**2 / 4 - (f.subs(x, b) - f.subs(x, a))**2 / (4 * M)
            diff = float((lhs_exact - rhs_exact).evalf())
            if diff > 1e-9:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the interval",
    "H_2: f is continuously differentiable on the interval",
    "¬Q: the integral inequality is violated"
]

N_HYP = 2
NEG_Q_INDEX = 2