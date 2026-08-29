import sympy
from sympy import Symbol, limit, oo, Abs, E, factorial

n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    try:
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            
        ratio = Abs(expr / expr.subs(n, n+1))
        R = limit(ratio, n, oo)
        
        if R == sympy.nan or R.has(sympy.AccumBounds) or R.has(sympy.Limit):
            root = Abs(expr)**(1/n)
            L = limit(root, n, oo)
            if L == 0:
                R = oo
            elif L == oo:
                R = 0
            elif not L.has(sympy.Limit):
                R = 1 / L
                
        if R.has(sympy.Limit) or R == sympy.nan:
            neg_q = False
        elif R == E:
            neg_q = False
        else:
            try:
                if hasattr(R, 'equals') and R.equals(E):
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to e"
]

N_HYP = 0
NEG_Q_INDEX = 0