import sympy
from sympy import Symbol, Interval, S, oo
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f is continuous on the interval",
    "¬Q: f does not attain a maximum on the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                f, domain = witness
                if not isinstance(domain, sympy.Set):
                    a, b = domain
                    domain = Interval(sympy.sympify(a), sympy.sympify(b))
            elif len(witness) == 3:
                f, a, b = witness
                domain = Interval(sympy.sympify(a), sympy.sympify(b))
            else:
                f = witness[0]
                domain = Interval(-oo, oo)
        else:
            f = witness
            domain = Interval(-oo, oo)
            
        f = sympy.sympify(f)
    except Exception:
        return [False, False]

    try:
        if hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
            var = list(f.free_symbols)[0]
        elif hasattr(f, 'free_symbols') and len(f.free_symbols) > 1:
            if x in f.free_symbols:
                var = x
            else:
                var = list(f.free_symbols)[0]
        else:
            var = x
    except Exception:
        var = x

    try:
        cont_dom = continuous_domain(f, var, domain)
        h1 = (domain.is_subset(cont_dom) == True)
    except Exception:
        h1 = False

    try:
        rng = function_range(f, var, domain)
        sup = rng.sup
        if sup == oo:
            neg_q = True
        else:
            neg_q = (rng.contains(sup) == False)
    except Exception:
        neg_q = False

    return [h1, neg_q]