import sympy
import math

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, a, b, L = witness
        df = sympy.diff(f, x)
        arc_length = sympy.Integral(sympy.sqrt(1 + df**2), (x, a, b)).evalf()
        bound = (b - a) * sympy.sqrt(1 + L**2)
        
        val_arc = float(sympy.re(arc_length))
        val_bound = float(sympy.re(bound))
        
        neg_q = bool(val_arc > val_bound)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["not Q: Arc length of f is strictly greater than the bound"]

N_HYP = 0
NEG_Q_INDEX = 0