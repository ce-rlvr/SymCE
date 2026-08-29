import sympy as sp
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, a, b = witness
        if callable(f):
            f = f(x)
    except Exception:
        return [False, False]
        
    try:
        if float(a) >= float(b):
            h1 = False
        else:
            integral_val = sp.integrate(f, (x, a, b))
            if integral_val.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                h1 = False
            else:
                float(integral_val.evalf())
                h1 = True
    except Exception:
        h1 = False

    try:
        integral_val = sp.integrate(f, (x, a, b))
        avg_val = integral_val / (b - a)
        
        mid_x = (a + b) / 2
        mid_val = f.subs(x, mid_x)
        
        ends_avg = (f.subs(x, a) + f.subs(x, b)) / 2
        
        diff1 = float((mid_val - avg_val).evalf())
        diff2 = float((avg_val - ends_avg).evalf())
        
        neg_q = (diff1 > 1e-7) or (diff2 > 1e-7)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is Riemann integrable on interval a to b",
    "not Q: Hermite-Hadamard inequality fails"
]

N_HYP = 1
NEG_Q_INDEX = 1