import sympy
from sympy import Symbol, limit, oo, Abs, factorial, gamma, Rational, Integer

n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def check_resolved(val):
    if not hasattr(val, 'is_number'):
        return False
    if not val.is_number:
        return False
    if val.has(sympy.nan):
        return False
    if type(val).__name__ == 'AccumBounds':
        return False
    return True

def conditions(witness):
    try:
        if callable(witness):
            a_n = witness(n)
        else:
            a_n = witness
            
        if a_n == 0:
            R = oo
        else:
            a_n_plus_1 = a_n.subs(n, n + 1)
            ratio = Abs(a_n / a_n_plus_1)
            R = limit(ratio, n, oo)
            
            if not check_resolved(R):
                root = Abs(a_n)**(1/n)
                L = limit(root, n, oo)
                if L == 0:
                    R = oo
                elif L == oo:
                    R = 0
                else:
                    R = 1 / L
                    
            if not check_resolved(R):
                val1 = float(Abs(a_n.subs(n, 100) / a_n.subs(n, 101)).evalf())
                val2 = float(Abs(a_n.subs(n, 200) / a_n.subs(n, 201)).evalf())
                if abs(val1 - 1) > 0.1 and abs(val2 - 1) > 0.1:
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = bool(R != 1)
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to 1"
]

N_HYP = 0
NEG_Q_INDEX = 0