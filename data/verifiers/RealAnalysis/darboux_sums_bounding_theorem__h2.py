import sympy
from sympy import Symbol, integrate, minimum, maximum, Interval, oo, zoo, nan
from sympy.abc import x

def conditions(witness):
    try:
        f, a, b, P = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        f = sympy.sympify(f)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        P = [sympy.sympify(p) for p in P]
    except Exception:
        return [False, False, False, False]

    var = x
    if hasattr(f, "free_symbols"):
        syms = list(f.free_symbols)
        if len(syms) > 0:
            var = syms[0]
        
    # H1: f is a bounded, Riemann integrable real-valued function on the interval
    h1 = False
    try:
        if a <= b:
            val = integrate(f, (var, a, b))
            if val.is_real and not val.has(oo, -oo, zoo, nan):
                h1 = True
    except Exception:
        pass
        
    # H2: L(f, P) is the lower Darboux sum
    h2 = False
    try:
        if isinstance(P, (list, tuple)) and len(P) >= 2:
            if all(P[i-1] <= P[i] for i in range(1, len(P))):
                h2 = True
    except Exception:
        pass
        
    # H3: U(f, P) is the upper Darboux sum
    h3 = h2
    
    # neg_Q: The conclusion L(f, P) <= int_a^b f(x) dx <= U(f, P) fails
    neg_q = False
    try:
        if h1 and h2 and h3:
            L = 0
            U = 0
            for i in range(1, len(P)):
                x_prev = P[i-1]
                x_curr = P[i]
                if x_prev == x_curr:
                    continue
                
                inf_val = minimum(f, var, Interval(x_prev, x_curr))
                sup_val = maximum(f, var, Interval(x_prev, x_curr))
                
                L += inf_val * (x_curr - x_prev)
                U += sup_val * (x_curr - x_prev)
            
            integral_val = integrate(f, (var, a, b))
            
            cond1 = bool(L <= integral_val)
            cond2 = bool(integral_val <= U)
            
            if not (cond1 and cond2):
                neg_q = True
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is bounded and Riemann integrable",
    "H_2: L is the lower Darboux sum",
    "H_3: U is the upper Darboux sum",
    "¬Q: Darboux sum bounds fail"
]

N_HYP = 3
NEG_Q_INDEX = 3