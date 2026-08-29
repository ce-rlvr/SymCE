import sympy
from sympy import Symbol, oo, zoo, AccumBounds, Abs
import math
import itertools
import functools

# Top-level setup: named object bindings
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    # H_1: (x_n) is a sequence of real numbers
    try:
        expr = sympy.sympify(witness)
        if not expr.free_symbols.issubset({n}):
            h1_ok = False
        else:
            h1_ok = True
            for i in range(1, 11):
                val = expr.subs(n, i).evalf()
                if not val.is_real:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: (x_n) is bounded
    try:
        expr = sympy.sympify(witness)
        try:
            L = sympy.limit(Abs(expr), n, oo)
            if isinstance(L, AccumBounds):
                h2_ok = (L.max < oo) and (L.min > -oo)
            else:
                if L.is_finite is True:
                    h2_ok = True
                elif L.is_finite is False:
                    h2_ok = False
                else:
                    h2_ok = not (L == oo or L == -oo or L == zoo or L.has(sympy.nan))
        except Exception:
            # Empirical fallback
            vals = []
            for i in range(1, 1000):
                v = expr.subs(n, i).evalf()
                if not v.is_real:
                    raise ValueError
                vals.append(float(abs(v)))
            h2_ok = max(vals) < 1e6
    except Exception:
        h2_ok = False

    # ¬Q: The sequence (x_n) is not convergent
    try:
        expr = sympy.sympify(witness)
        try:
            L = sympy.limit(expr, n, oo)
            if isinstance(L, AccumBounds):
                neg_q_ok = (L.min != L.max)
            else:
                if L.is_finite is True:
                    neg_q_ok = False
                elif L.is_finite is False:
                    neg_q_ok = True
                else:
                    neg_q_ok = (L == oo or L == -oo or L == zoo or L.has(sympy.nan))
        except Exception:
            # Empirical fallback: check if sequence is Cauchy
            vals = []
            for i in range(1000, 1050):
                v = expr.subs(n, i).evalf()
                if not v.is_real:
                    raise ValueError
                vals.append(float(v))
            
            is_cauchy = True
            for i in range(len(vals)):
                for j in range(i+1, len(vals)):
                    if abs(vals[i] - vals[j]) > 1e-4:
                        is_cauchy = False
                        break
                if not is_cauchy:
                    break
            neg_q_ok = not is_cauchy
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: (x_n) is bounded",
    "¬Q: The sequence (x_n) is not convergent"
]

N_HYP = 2
NEG_Q_INDEX = 2