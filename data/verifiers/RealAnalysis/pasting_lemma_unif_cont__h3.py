import sympy
import math
import itertools
import functools

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        a, b, c, f = witness
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        c_sym = sympy.sympify(c)
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are real numbers with a < b < c
    try:
        if a_sym.is_real and b_sym.is_real and c_sym.is_real:
            h1 = bool(a_sym < b_sym) and bool(b_sym < c_sym)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: f is uniformly continuous on the interval a to b
    try:
        if callable(f):
            f_sym = sympy.sympify(f(x))
        else:
            f_sym = sympy.sympify(f)
            
        free_symbols = f_sym.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = x
        else:
            if x in free_symbols:
                var = x
            else:
                var = list(free_symbols)[0]
                
        from sympy.calculus.util import continuous_domain
        domain_ab = continuous_domain(f_sym, var, sympy.Interval(a_sym, b_sym))
        subset_check = sympy.Interval(a_sym, b_sym).is_subset(domain_ab)
        h2 = (subset_check is True)
    except Exception:
        h2 = False

    # neg_Q: f is not uniformly continuous on the interval a to c
    try:
        if callable(f):
            f_sym = sympy.sympify(f(x))
        else:
            f_sym = sympy.sympify(f)
            
        free_symbols = f_sym.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = x
        else:
            if x in free_symbols:
                var = x
            else:
                var = list(free_symbols)[0]
                
        from sympy.calculus.util import continuous_domain
        domain_ac = continuous_domain(f_sym, var, sympy.Interval(a_sym, c_sym))
        subset_check = sympy.Interval(a_sym, c_sym).is_subset(domain_ac)
        neg_q = (subset_check is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are real numbers with a < b < c",
    "H_2: f is uniformly continuous on the interval a to b",
    "¬Q: f is not uniformly continuous on the interval a to c"
]

N_HYP = 2
NEG_Q_INDEX = 2