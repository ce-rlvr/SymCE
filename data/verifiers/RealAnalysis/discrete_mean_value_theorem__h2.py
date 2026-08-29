import sympy
from sympy.abc import x
from sympy.calculus.util import continuous_domain, minimum, maximum
from sympy import Interval, S

def conditions(witness):
    try:
        f, a, b, w_list, x_list = witness
        f = sympy.sympify(f)
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
    except Exception:
        return [False, False, False, False]

    try:
        a_val = float(a_sym.evalf())
        b_val = float(b_sym.evalf())
        if a_val > b_val:
            h1 = False
        else:
            domain = continuous_domain(f, x, S.Reals)
            h1 = bool(Interval(a_sym, b_sym).is_subset(domain))
    except Exception:
        h1 = False

    try:
        h2 = True
        for w in w_list:
            w_val = sympy.sympify(w)
            if not w_val.is_number:
                h2 = False
                break
            if not bool(w_val >= 0):
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        total_w = sum(sympy.sympify(w) for w in w_list)
        if total_w.is_number:
            h3 = bool(sympy.simplify(total_w - 1) == 0)
            if not h3:
                h3 = bool(abs(float(total_w.evalf()) - 1.0) < 1e-9)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if len(w_list) != len(x_list) or len(w_list) == 0:
            neg_q = False
        else:
            V = sum(sympy.sympify(w) * f.subs(x, sympy.sympify(xi)) for w, xi in zip(w_list, x_list))
            
            neg_q = None
            try:
                sols = sympy.solveset(f - V, x, domain=Interval(a_sym, b_sym))
                if sols.is_empty is True:
                    neg_q = True
                elif sols.is_empty is False:
                    neg_q = False
            except Exception:
                pass
                
            if neg_q is None:
                f_min = minimum(f, x, Interval(a_sym, b_sym))
                f_max = maximum(f, x, Interval(a_sym, b_sym))
                
                V_val = float(sympy.sympify(V).evalf())
                f_min_val = float(sympy.sympify(f_min).evalf())
                f_max_val = float(sympy.sympify(f_max).evalf())
                
                neg_q = bool(V_val < f_min_val - 1e-9 or V_val > f_max_val + 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "H_2: w_i are non-negative real numbers",
    "H_3: sum of w_i is exactly 1",
    "¬Q: There is no c in the interval such that f(c) equals the weighted sum"
]

N_HYP = 3
NEG_Q_INDEX = 3