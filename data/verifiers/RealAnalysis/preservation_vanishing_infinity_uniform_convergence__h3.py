import sympy
from sympy import Symbol, limit, oo

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions defined on R",
    "H_2: For each n, lim_{|x| -> oo} f_n(x) = 0",
    "¬Q: The limit function f does not satisfy lim_{|x| -> oo} f(x) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if callable(witness):
            expr = witness(n, x)
        else:
            expr = witness
    except Exception:
        expr = witness

    # H_1: (f_n) is a sequence of real-valued functions defined on R
    try:
        h1 = True
        for nv in [1, 2, 3]:
            fn = expr.subs(n, nv)
            # Evaluate at a few sample points to ensure it's real-valued and finite
            for xv in [0.0, 1.5, -2.5, 3.1415926535]:
                val = fn.subs(x, xv).evalf()
                try:
                    cval = complex(val)
                    if abs(cval.imag) > 1e-9:
                        h1 = False
                        break
                except Exception:
                    # If it cannot be converted to complex (e.g., infinity or undefined), it fails
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: For each n, lim_{|x| -> oo} f_n(x) = 0
    try:
        h2 = True
        for nv in [1, 2, 3, 4, 5]:
            fn = expr.subs(n, nv)
            lim_pos = limit(fn, x, oo)
            lim_neg = limit(fn, x, -oo)
            if lim_pos != 0 or lim_neg != 0:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The limit function f does not satisfy lim_{|x| -> oo} f(x) = 0
    try:
        f = limit(expr, n, oo)
        if f.has(sympy.Limit):
            # If sympy cannot evaluate the pointwise limit, we conservatively return False
            neg_q = False
        else:
            lim_f_pos = limit(f, x, oo)
            lim_f_neg = limit(f, x, -oo)
            
            if lim_f_pos.has(sympy.Limit) or lim_f_neg.has(sympy.Limit):
                neg_q = False
            else:
                neg_q = (lim_f_pos != 0) or (lim_f_neg != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]