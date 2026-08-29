import sympy
from sympy import Symbol, S, diff, limit, oo
from sympy.calculus.util import continuous_domain, function_range

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f, D = witness
    except Exception:
        return [False, False]
        
    if callable(f):
        try:
            f = f(x)
        except Exception:
            pass

    # H1: f is uniformly continuous on D
    h1_ok = False
    try:
        is_cont = False
        try:
            if continuous_domain(f, x, D) == D:
                is_cont = True
        except Exception:
            pass
            
        if is_cont:
            df = diff(f, x)
            if df.is_constant():
                h1_ok = True
            else:
                try:
                    frange = function_range(df, x, D)
                    if frange.inf > -oo and frange.sup < oo:
                        h1_ok = True
                except Exception:
                    pass
    except Exception:
        pass

    # neg_Q: f is NOT bounded on D
    neg_q_ok = False
    try:
        try:
            frange = function_range(f, x, D)
            if frange.inf == -oo or frange.sup == oo:
                neg_q_ok = True
        except Exception:
            pass
            
        if not neg_q_ok:
            try:
                if D.sup == oo:
                    L = limit(f, x, oo)
                    if L == oo or L == -oo:
                        neg_q_ok = True
                if D.inf == -oo:
                    L = limit(f, x, -oo)
                    if L == oo or L == -oo:
                        neg_q_ok = True
            except Exception:
                pass
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on D",
    "¬Q: f is not bounded on D"
]

N_HYP = 1
NEG_Q_INDEX = 1