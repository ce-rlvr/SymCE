import sympy
from sympy import Symbol, Interval, integrate
from sympy.calculus.util import minimum, continuous_domain
import math
import itertools
import functools
import z3

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        
        f_raw, a_raw, b_raw = witness
        
        if callable(f_raw):
            f_raw = f_raw(x)
            
        f = sympy.sympify(f_raw)
        a = sympy.sympify(a_raw)
        b = sympy.sympify(b_raw)
        
        free_syms = f.free_symbols
        if len(free_syms) > 1:
            return [False, False, False]
        elif len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = x
    except Exception:
        return [False, False, False]

    try:
        if float(a) >= float(b):
            h1 = False
        else:
            domain = continuous_domain(f, var, Interval(a, b))
            h1 = (domain == Interval(a, b))
    except Exception:
        h1 = False

    try:
        fa = sympy.simplify(f.subs(var, a))
        fb = sympy.simplify(f.subs(var, b))
        h2 = (fa == 0 and fb == 0)
        if not h2:
            h2 = bool(abs(float(fa)) < 1e-12 and abs(float(fb)) < 1e-12)
    except Exception:
        h2 = False

    try:
        integral_val = integrate(f, (var, a, b))
        min_f = minimum(f, var, Interval(a, b))
        rhs = (b - a) / 2 * min_f
        
        diff = sympy.simplify(integral_val - rhs)
        if diff.is_positive is True:
            neg_q = True
        elif diff.is_positive is False:
            neg_q = False
        else:
            neg_q = bool(diff.evalf() > 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval from a to b",
    "H_2: f(a) = 0 and f(b) = 0",
    "¬Q: integral of f > (b-a)/2 * min f"
]

N_HYP = 2
NEG_Q_INDEX = 2