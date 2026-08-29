import sympy
from sympy import diff, simplify, limit, oo, S, Limit
from sympy.abc import x, n
from sympy.calculus.util import maximum, continuous_domain

# Top-level setup: x and n are available for witness expressions
# The witness should be a tuple (f, c) where f is an expression in x 
# and c is an expression in n (representing the sequence c_n).

def conditions(witness):
    try:
        f, c = witness
        # c_n should be a sequence independent of x
        if hasattr(c, 'free_symbols') and x in c.free_symbols:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H1: f is uniformly continuous on R
    h1_ok = False
    try:
        df = diff(f, x)
        if df.is_constant():
            h1_ok = True
        else:
            try:
                max_val = maximum(df**2, x, S.Reals)
                if max_val < oo:
                    h1_ok = True
            except Exception:
                pass
    except Exception:
        h1_ok = False

    # neg_Q: f(x + c_n) does NOT converge uniformly to f(x)
    neg_q_ok = False
    try:
        g = simplify(f.subs(x, x + c) - f)
        if not g.has(x):
            lim_g = limit(g, n, oo)
            if not (hasattr(lim_g, 'has') and lim_g.has(Limit)):
                if lim_g != 0:
                    neg_q_ok = True
        else:
            # Pointwise check at a few points (if pointwise fails, uniform fails)
            for pt in [0, 1, -1, 2, sympy.pi]:
                try:
                    lim_g_pt = limit(g.subs(x, pt), n, oo)
                    if not (hasattr(lim_g_pt, 'has') and lim_g_pt.has(Limit)):
                        if lim_g_pt != 0:
                            neg_q_ok = True
                            break
                except Exception:
                    pass
            else:
                # Uniform check if pointwise limits are 0
                try:
                    max_g2 = maximum(g**2, x, S.Reals)
                    lim_max = limit(max_g2, n, oo)
                    if not (hasattr(lim_max, 'has') and lim_max.has(Limit)):
                        if lim_max != 0:
                            neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a uniformly continuous function on R",
    "¬Q: The sequence of translated functions f_n(x) = f(x + c_n) does not converge uniformly to f(x) on R"
]

N_HYP = 1
NEG_Q_INDEX = 1