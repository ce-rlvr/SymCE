import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def conditions(witness):
    try:
        # Evaluate the witness to get the n-th coefficient
        if callable(witness):
            try:
                a_n = witness(n)
            except Exception:
                a_n = witness(n, x)
        else:
            a_n = witness
            
        a_n = sympy.sympify(a_n)
        
        # If the witness was given as a_n * x**n, extract a_n by setting x to 1
        if a_n.has(x):
            a_n = a_n.subs(x, 1)
            
        # Try the ratio test first
        try:
            ratio = sympy.Abs(a_n / a_n.subs(n, n + 1))
            R = sympy.limit(ratio, n, sympy.oo)
        except Exception:
            R = sympy.nan
            
        # If the ratio test fails or is inconclusive, try the root test
        if R is sympy.nan or R.has(sympy.nan) or not (R.is_number or R == sympy.oo):
            try:
                root = sympy.Abs(a_n)**(1/n)
                L = sympy.limit(root, n, sympy.oo)
                if L == 0:
                    R = sympy.oo
                elif L == sympy.oo:
                    R = 0
                else:
                    R = 1 / L
            except Exception:
                R = sympy.nan
                
        # Evaluate the negated conclusion: R != 1
        if R is sympy.nan or R.has(sympy.nan):
            neg_q = False
        elif R == 1:
            neg_q = False
        elif R.is_number or R == sympy.oo:
            neg_q = True
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of the power series is not equal to 1"
]

N_HYP = 0
NEG_Q_INDEX = 0