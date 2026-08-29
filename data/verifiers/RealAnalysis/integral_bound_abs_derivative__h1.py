import sympy
from sympy import Abs, integrate, diff, Piecewise, Symbol, oo, re
import math
import itertools
import functools

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f, a, b = witness
        else:
            f = witness
            a, b = -1, 1
            
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
            
        lhs = Abs(f_expr.subs(x, b) - f_expr.subs(x, a))
        df = diff(f_expr, x)
        rhs = integrate(Abs(df), (x, a, b))
        
        if rhs == oo:
            neg_q = False
        else:
            lhs_val = float(re(lhs.evalf()))
            rhs_val = float(re(rhs.evalf()))
            neg_q = bool(lhs_val > rhs_val + 1e-9)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: |f(b) - f(a)| > \\int_a^b |f'(x)| dx"
]
N_HYP = 0
NEG_Q_INDEX = 0