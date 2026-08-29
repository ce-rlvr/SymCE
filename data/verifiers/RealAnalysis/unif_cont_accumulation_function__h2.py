import sympy
from sympy.calculus.util import continuous_domain

CONDITION_LABELS = [
    "H_1: f is Riemann integrable",
    "¬Q: F is not uniformly continuous"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if len(witness) == 4:
            f, x_sym, a, b = witness
            f = sympy.sympify(f)
            x_sym = sympy.sympify(x_sym)
            a = sympy.sympify(a)
            b = sympy.sympify(b)
        elif len(witness) == 3:
            f, a, b = witness
            f = sympy.sympify(f)
            a = sympy.sympify(a)
            b = sympy.sympify(b)
            free = f.free_symbols
            if len(free) == 1:
                x_sym = list(free)[0]
            else:
                x_sym = sympy.Symbol('x', real=True)
        else:
            return [False, False]
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        integral_val = sympy.integrate(f, (x_sym, a, b))
        if integral_val.is_finite:
            h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        t_sym = sympy.Symbol('t', real=True)
        f_t = f.subs(x_sym, t_sym)
        F = sympy.integrate(f_t, (t_sym, a, x_sym))
        
        is_unif_cont = True
        domain = sympy.Interval(a, b)
        
        cont_dom = continuous_domain(F, x_sym, domain)
        if not domain.is_subset(cont_dom):
            is_unif_cont = False
            
        if is_unif_cont:
            if b == sympy.oo:
                lim_b = sympy.limit(F, x_sym, sympy.oo)
                if not lim_b.is_finite:
                    is_unif_cont = False
            if a == -sympy.oo:
                lim_a = sympy.limit(F, x_sym, -sympy.oo)
                if not lim_a.is_finite:
                    is_unif_cont = False
                    
        neg_q_ok = not is_unif_cont
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]