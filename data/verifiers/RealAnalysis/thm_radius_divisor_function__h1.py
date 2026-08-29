import sympy
from sympy import Symbol, limit, oo, Abs

n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    neg_q = False
    try:
        if isinstance(witness, (list, tuple)):
            R = oo
        else:
            if callable(witness):
                expr = witness(n)
            else:
                expr = witness
                
            expr = sympy.sympify(expr, locals={'n': n})
            
            if expr == 0:
                R = oo
            else:
                ratio = Abs(expr / expr.subs(n, n + 1))
                R = limit(ratio, n, oo)
                
                if not (R == oo or R == sympy.zoo or (hasattr(R, 'is_number') and R.is_number)):
                    root = Abs(expr)**(1/n)
                    R = limit(1/root, n, oo)
                    
        if R == oo or R == sympy.zoo:
            neg_q = True
        elif hasattr(R, 'is_number') and R.is_number:
            neg_q = bool(sympy.simplify(R - 1) != 0)
        elif isinstance(R, (int, float)):
            neg_q = bool(abs(float(R) - 1.0) > 1e-8)
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to 1"
]

N_HYP = 0
NEG_Q_INDEX = 0