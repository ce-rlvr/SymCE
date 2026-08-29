import sympy as sp
from sympy.abc import x
import math

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple: (f, a, b, M)
    where f is a sympy expression in terms of x, and a, b, M are real numbers.
    """
    try:
        f, a, b, M = witness
        f = sp.sympify(f)
        a = float(a)
        b = float(b)
        M = float(M)
    except Exception:
        return [False, False, False]

    # H_1: f is a continuously differentiable real-valued function on the interval
    try:
        if a >= b:
            h1 = False
        else:
            df = sp.diff(f, x)
            df_lam = sp.lambdify(x, df, 'math')
            h1 = True
            for i in range(101):
                val = a + (b - a) * i / 100.0
                try:
                    v = df_lam(val)
                    if not math.isfinite(v):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: There exists a real number M > 0 such that abs(df/dx) <= M for all x
    try:
        if M <= 0:
            h2 = False
        else:
            df = sp.diff(f, x)
            df_lam = sp.lambdify(x, df, 'math')
            h2 = True
            for i in range(1001):
                val = a + (b - a) * i / 1000.0
                if abs(df_lam(val)) > M + 1e-7:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # not Q: Integral of abs(f(x)) from a to b > M(b-a)^2 / 4
    try:
        f_lam = sp.lambdify(x, f, 'math')
        integral_val = 0.0
        N_steps = 2000
        dx = (b - a) / N_steps
        for i in range(N_steps):
            mid = a + (i + 0.5) * dx
            integral_val += abs(f_lam(mid)) * dx
            
        rhs = M * (b - a)**2 / 4.0
        neg_q = integral_val > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable real-valued function on the interval",
    "H_2: There exists a real number M > 0 such that abs(df/dx) <= M for all x",
    "not Q: Integral of abs(f(x)) from a to b > M(b-a)^2 / 4"
]

N_HYP = 2
NEG_Q_INDEX = 2