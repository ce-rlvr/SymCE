import sympy
from sympy import limit, oo, Abs, log

# Top-level setup
n = sympy.Symbol('n', integer=True, positive=True)
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any sequence a_n and any R, the power series 
    sum_{n=2}^infty a_n ln(n) x^n has a radius of convergence equal to R.
    (The hypothesis that sum a_n x^n has radius of convergence R was dropped).
    
    A valid witness is a tuple (a_n, R) where a_n is a sympy expression in terms of n 
    (or a callable returning one) and R is the claimed radius of convergence.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False]
        
        a_n_input, R_input = witness
        
        if callable(a_n_input):
            a_n = a_n_input(n)
        else:
            a_n = sympy.sympify(a_n_input)
            
        R = sympy.sympify(R_input)
            
        if sympy.simplify(a_n) == 0:
            R_actual = oo
        else:
            b_n = a_n * log(n)
            
            # Try ratio test
            ratio = Abs(b_n.subs(n, n+1) / b_n)
            L = limit(ratio, n, oo)
            
            if not (L.is_number or L == oo):
                # Fallback to root test
                root = Abs(b_n)**(1/n)
                L = limit(root, n, oo)
                
            if not (L.is_number or L == oo):
                return [False]
                
            if L == 0:
                R_actual = oo
            elif L == oo:
                R_actual = sympy.S(0)
            else:
                R_actual = 1 / L
            
        # Check if the actual radius of convergence equals R
        if R_actual == oo and R == oo:
            neg_q = False
        elif R_actual == oo or R == oo:
            neg_q = True
        else:
            diff = sympy.simplify(R_actual - R)
            neg_q = (diff != 0)
            
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The radius of convergence of sum a_n ln(n) x^n is not equal to R"
]

N_HYP = 0
NEG_Q_INDEX = 0