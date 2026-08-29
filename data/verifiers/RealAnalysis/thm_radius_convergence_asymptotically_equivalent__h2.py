import sympy
from sympy import Symbol, limit, oo, Abs

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: sum a_n x^n and sum b_n x^n are power series",
    "H_2: The limit lim_{n -> oo} |a_n / b_n| exists and equals a real number L such that 0 < L < oo",
    "not Q: The two power series do not have the exact same radius of convergence"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if callable(witness[0]):
            a_n = witness[0](n)
            b_n = witness[1](n)
        else:
            a_n, b_n = witness
            
        # Ensure they are sympy expressions
        a_n = sympy.sympify(a_n)
        b_n = sympy.sympify(b_n)
        
        # If the witness includes x**n, extract the coefficient by substituting x=1
        if a_n.has(x):
            a_n = a_n.subs(x, 1)
        if b_n.has(x):
            b_n = b_n.subs(x, 1)
    except Exception:
        return [False, False, False]
        
    # H1: a_n and b_n are power series coefficients
    h1 = True
    
    # H2: limit |a_n / b_n| exists and is in (0, oo)
    try:
        L = limit(Abs(a_n / b_n), n, oo)
        if L.has(sympy.Limit) or type(L).__name__ == 'AccumBounds':
            h2 = False
        else:
            h2 = bool(L.is_real and L > 0 and L < oo)
    except Exception:
        h2 = False
        
    # neg_Q: R_a != R_b
    try:
        def get_radius(c_n):
            root_lim = limit(Abs(c_n)**(1/n), n, oo)
            if root_lim.has(sympy.Limit):
                raise ValueError("Could not evaluate limit")
            
            if type(root_lim).__name__ == 'AccumBounds':
                limsup = root_lim.max
            else:
                limsup = root_lim
                
            if limsup == 0:
                return oo
            elif limsup == oo:
                return 0
            else:
                return 1 / limsup
                
        R_a = get_radius(a_n)
        R_b = get_radius(b_n)
        
        if R_a == oo and R_b == oo:
            neg_q = False
        elif R_a == oo or R_b == oo:
            neg_q = True
        else:
            diff = sympy.simplify(R_a - R_b)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]