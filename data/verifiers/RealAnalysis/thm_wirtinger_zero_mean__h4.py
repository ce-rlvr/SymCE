import sympy as sp
from sympy.calculus.util import continuous_domain

x = sp.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        witness = sp.sympify(witness)
    except Exception:
        return [False, False, False, False]

    try:
        dom = continuous_domain(witness, x, sp.Interval(0, 2*sp.pi))
        h1 = bool(dom == sp.Interval(0, 2*sp.pi))
    except Exception:
        h1 = False

    try:
        val0 = witness.subs(x, 0)
        val2pi = witness.subs(x, 2*sp.pi)
        diff_val = sp.simplify(val0 - val2pi)
        h2 = bool(diff_val == 0) or float(sp.Abs(diff_val).evalf()) < 1e-9
    except Exception:
        h2 = False

    try:
        df = sp.diff(witness, x)
        int_df2 = sp.integrate(df**2, (x, 0, 2*sp.pi)).evalf()
        h3 = float(sp.re(int_df2)) < float('inf')
    except Exception:
        h3 = False

    try:
        df = sp.diff(witness, x)
        diff_val = sp.integrate(witness**2 - df**2, (x, 0, 2*sp.pi)).evalf()
        neg_q = float(sp.re(diff_val)) > 1e-7
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is absolutely continuous on 0 to 2pi",
    "H_2: f(0) = f(2pi)",
    "H_3: f prime in L2",
    "not Q: int f^2 > int f prime^2"
]

N_HYP = 3
NEG_Q_INDEX = 3