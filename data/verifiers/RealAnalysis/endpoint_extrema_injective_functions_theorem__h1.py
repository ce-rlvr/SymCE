import sympy as sp
from sympy import Symbol, Interval, S
from sympy.calculus.util import continuous_domain, maximum, minimum
from sympy.calculus.singularities import is_strictly_increasing, is_strictly_decreasing

CONDITION_LABELS = [
    "H_1: f is continuous at every point in the interval",
    "H_2: f is injective on the interval",
    "¬Q: The absolute maximum and absolute minimum of f do not both occur at the endpoints"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness
    except Exception:
        return [False, False, False]

    try:
        f = sp.sympify(f)
        a = sp.sympify(a)
        b = sp.sympify(b)
        
        if not a.is_real or not b.is_real:
            return [False, False, False]
            
        if a.is_number and b.is_number:
            is_empty = bool(a > b)
            is_point = bool(a == b)
        else:
            is_empty = False
            is_point = False
    except Exception:
        return [False, False, False]

    try:
        if hasattr(f, 'free_symbols'):
            free_syms = f.free_symbols
            real_syms = [s for s in free_syms if s.is_real is not False]
            if len(real_syms) == 1:
                x = real_syms[0]
            elif len(free_syms) == 1:
                x = list(free_syms)[0]
            elif len(free_syms) == 0:
                x = Symbol('x', real=True)
            else:
                return [False, False, False]
        else:
            x = Symbol('x', real=True)
    except Exception:
        return [False, False, False]

    # H1: f is continuous at every point in the interval
    try:
        if is_empty:
            h1 = True
        else:
            domain = Interval(a, b)
            cond_domain = continuous_domain(f, x, S.Reals)
            h1 = bool(domain.is_subset(cond_domain))
    except Exception:
        h1 = False

    # H2: f is injective on the interval
    try:
        if is_empty or is_point:
            h2 = True
        else:
            domain = Interval(a, b)
            inc = is_strictly_increasing(f, domain, x)
            dec = is_strictly_decreasing(f, domain, x)
            h2 = bool(inc or dec)
    except Exception:
        h2 = False

    # ¬Q: The absolute maximum and absolute minimum of f do NOT both occur at the endpoints
    try:
        if is_empty:
            neg_q = True
        elif is_point:
            neg_q = False
        else:
            domain = Interval(a, b)
            f_max = maximum(f, x, domain)
            f_min = minimum(f, x, domain)
            
            max_at_a = sp.simplify(f.subs(x, a) - f_max) == 0
            if not max_at_a:
                try: max_at_a = abs(float(f.subs(x, a) - f_max)) < 1e-9
                except Exception: pass
            
            max_at_b = sp.simplify(f.subs(x, b) - f_max) == 0
            if not max_at_b:
                try: max_at_b = abs(float(f.subs(x, b) - f_max)) < 1e-9
                except Exception: pass

            min_at_a = sp.simplify(f.subs(x, a) - f_min) == 0
            if not min_at_a:
                try: min_at_a = abs(float(f.subs(x, a) - f_min)) < 1e-9
                except Exception: pass

            min_at_b = sp.simplify(f.subs(x, b) - f_min) == 0
            if not min_at_b:
                try: min_at_b = abs(float(f.subs(x, b) - f_min)) < 1e-9
                except Exception: pass
            
            max_at_endpoints = max_at_a or max_at_b
            min_at_endpoints = min_at_a or min_at_b
            
            neg_q = not (max_at_endpoints and min_at_endpoints)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]