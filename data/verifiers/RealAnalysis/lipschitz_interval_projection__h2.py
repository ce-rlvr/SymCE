import math
import sympy
from sympy import Rational

# Top-level setup
x_sym, y_sym, z_sym = sympy.symbols('x y z')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            P = witness['P']
            x = witness['x']
            y = witness['y']
        elif isinstance(witness, (tuple, list)):
            a, b, P, x, y = witness
        else:
            a = witness.a
            b = witness.b
            P = witness.P
            x = witness.x
            y = witness.y
    except Exception:
        return [False, False]

    try:
        h1 = False
        fa = float(a)
        fb = float(b)
        if fa <= fb:
            h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        fx = float(x)
        fy = float(y)
        
        if callable(P):
            px = float(P(x))
            py = float(P(y))
        elif isinstance(P, dict):
            px = float(P[x])
            py = float(P[y])
        else:
            syms = list(P.free_symbols)
            if len(syms) >= 1:
                sym = syms[0]
                px = float(P.subs(sym, x))
                py = float(P.subs(sym, y))
            else:
                px = float(P)
                py = float(P)
                
        if abs(px - py) > abs(fx - fy):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: interval a to b is a closed interval in R", "¬Q: abs(P(x) - P(y)) > abs(x - y)"]

N_HYP = 1
NEG_Q_INDEX = 1