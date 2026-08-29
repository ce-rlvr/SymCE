import sympy
from sympy import Symbol, Interval, S, EmptySet

x = Symbol('x')

def conditions(witness):
    try:
        f, a, b = witness
    except Exception:
        return [False, False]

    h1 = False
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        f_sym = sympy.sympify(f)
        
        if a_sym.is_real and b_sym.is_real and a_sym < b_sym:
            try:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(f_sym, x, S.Reals)
                h1 = bool(Interval(a_sym, b_sym).is_subset(dom))
            except Exception:
                if f_sym.is_polynomial(x):
                    h1 = True
    except Exception:
        h1 = False

    neg_q = False
    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        f_sym = sympy.sympify(f)
        if a_sym.is_real and b_sym.is_real and a_sym < b_sym:
            sols = sympy.solveset(f_sym - x, x, domain=Interval(a_sym, b_sym))
            if sols is EmptySet:
                neg_q = True
            elif sols.is_empty is False:
                neg_q = False
            else:
                try:
                    roots = sympy.real_roots(f_sym - x)
                    has_root = any(a_sym <= r <= b_sym for r in roots)
                    neg_q = not has_root
                except Exception:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function continuous on the closed interval from a to b",
    "¬Q: There is no point c in the closed interval from a to b such that f(c) = c"
]

N_HYP = 1
NEG_Q_INDEX = 1