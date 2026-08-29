import sympy
import math
import itertools
import functools
from sympy import *
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f', witness.get('function'))
            a = witness['a']
            b = witness['b']
            m = witness['m']
            M = witness['M']
        else:
            f, a, b, m, M = witness
            
        if callable(f):
            x_sym = sympy.Symbol('x')
            f = f(x_sym)
        f = sympy.sympify(f)
        a = float(a)
        b = float(b)
        m = float(m)
        M = float(M)
    except Exception:
        return [False, False]
    
    # H1: f is a Riemann integrable real-valued function on the closed interval a to b
    h1 = False
    val_f = 0.0
    val_f2 = 0.0
    try:
        if a < b:
            symbols = f.free_symbols
            if len(symbols) <= 1:
                sym_x = list(symbols)[0] if symbols else sympy.Symbol('x')
                int_f = sympy.integrate(f, (sym_x, a, b)).evalf()
                int_f2 = sympy.integrate(f**2, (sym_x, a, b)).evalf()
                
                val_f = float(int_f)
                val_f2 = float(int_f2)
                
                is_real_valued = True
                for i in range(11):
                    pt = a + (b - a) * i / 10.0
                    val = complex(f.subs(sym_x, pt).evalf())
                    if abs(val.imag) > 1e-9:
                        is_real_valued = False
                        break
                
                if is_real_valued and math.isfinite(val_f) and math.isfinite(val_f2):
                    h1 = True
    except Exception:
        h1 = False

    # neg_Q: Variance > (M - m)^2 / 4
    neg_q = False
    try:
        if h1:
            variance = val_f2 / (b - a) - (val_f / (b - a))**2
            bound = (M - m)**2 / 4.0
            if variance > bound + 1e-9:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a Riemann integrable real-valued function on the closed interval a to b",
    "¬Q: The variance of f exceeds (M-m)^2/4"
]

N_HYP = 1
NEG_Q_INDEX = 1