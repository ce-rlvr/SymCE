import sympy
from sympy import Symbol, Poly, Expr

x = Symbol('x')

def conditions(witness):
    h1 = False
    neg_q = True
    
    try:
        f = None
        E = None
        if isinstance(witness, tuple) and len(witness) == 2:
            f, E = witness
        elif isinstance(witness, (Expr, Poly)):
            f = witness
        else:
            E = witness

        if f is not None:
            if isinstance(f, Poly):
                f = f.as_expr()
            h1 = bool(sympy.simplify(f - (x**3 - 2)) == 0)
        else:
            h1 = True

        if E is not None:
            deg = None
            if hasattr(E, 'ext_degree'):
                deg = E.ext_degree
            elif hasattr(E, 'degree'):
                deg = E.degree
            
            if deg is not None:
                if callable(deg):
                    deg = deg()
                if int(deg) == 6:
                    neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f(x) = x**3 - 2 is a polynomial over Q", "¬Q: The splitting field E is not Q(cbrt(2), sqrt(-3)) or degree of E over Q is not 6"]
N_HYP = 1
NEG_Q_INDEX = 1