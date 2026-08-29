import sympy
from sympy.abc import x
import math

def eval_f(f, val):
    if hasattr(f, 'free_symbols'):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            return float(f.subs(syms[0], val))
        elif len(syms) == 0:
            return float(f)
        else:
            return float(f.subs(x, val))
    elif hasattr(f, 'subs'):
        return float(f.subs(x, val))
    else:
        return float(f(val))

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
        else:
            f, a, b = witness
            
        if isinstance(f, str):
            f = sympy.sympify(f)
    except Exception:
        return [False, False]
    
    h1_ok = False
    try:
        a_f = float(sympy.sympify(a))
        b_f = float(sympy.sympify(b))
        if a_f >= b_f:
            h1_ok = False
        else:
            rigorous_success = False
            if hasattr(f, 'free_symbols'):
                try:
                    from sympy.calculus.util import continuous_domain
                    from sympy.sets import Interval
                    syms = list(f.free_symbols)
                    sym = syms[0] if len(syms) == 1 else x
                    a_sym = sympy.sympify(a)
                    b_sym = sympy.sympify(b)
                    dom = continuous_domain(f, sym, Interval(a_sym, b_sym))
                    if Interval(a_sym, b_sym).is_subset(dom):
                        h1_ok = True
                    else:
                        h1_ok = False
                    rigorous_success = True
                except Exception:
                    pass
            
            if not rigorous_success:
                h1_ok = True
                for i in range(101):
                    val = a_f + (b_f - a_f) * i / 100.0
                    v = eval_f(f, val)
                    if math.isnan(v) or math.isinf(v):
                        h1_ok = False
                        break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        a_f = float(sympy.sympify(a))
        b_f = float(sympy.sympify(b))
        if a_f < b_f:
            vals = set()
            for i in range(1001):
                val = a_f + (b_f - a_f) * i / 1000.0
                v = eval_f(f, val)
                vals.add(math.floor(v))
                if len(vals) > 1:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a continuous function on the interval",
    "¬Q: g(x) = floor(f(x)) is not constant on the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1