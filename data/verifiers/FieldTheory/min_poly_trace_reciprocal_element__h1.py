import sympy
from sympy import Rational, Integer

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    x = sympy.Symbol('x')
    h1, h2, h3, h4, neg_q = False, False, False, False, False
    try:
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            alpha = sympy.Matrix(witness)
            try:
                m = alpha.minimal_polynomial(x)
            except Exception:
                m = alpha.charpoly(x).as_expr()
                
            n = sympy.degree(m, x)
            h1 = bool(n > 1)
            
            m_recip = sympy.expand(x**n * m.subs(x, 1/x))
            h2 = bool(sympy.expand(m_recip - m) == 0)
            
            I = sympy.eye(alpha.shape[0])
            h3 = bool(alpha != I)
            h4 = bool(alpha != -I)
            
            alpha_inv = alpha.inv()
            beta = alpha + alpha_inv
            try:
                m_beta = beta.minimal_polynomial(x)
            except Exception:
                m_beta = beta.charpoly(x).as_expr()
                
            deg_beta = sympy.degree(m_beta, x)
            neg_q = bool(2 * deg_beta != n)
            
        else:
            alpha = sympy.sympify(witness)
            m = sympy.minpoly(alpha, x)
            n = sympy.degree(m, x)
            
            h1 = bool(n > 1)
            
            m_recip = sympy.expand(x**n * m.subs(x, 1/x))
            h2 = bool(sympy.expand(m_recip - m) == 0)
            
            h3 = bool(alpha != 1)
            h4 = bool(alpha != -1)
            
            beta = alpha + 1/alpha
            m_beta = sympy.minpoly(beta, x)
            deg_beta = sympy.degree(m_beta, x)
            neg_q = bool(2 * deg_beta != n)
            
    except Exception:
        pass
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: The minimal polynomial m(x) of alpha over F has degree n > 1",
    "H_2: m(x) satisfies the reciprocal property x^n m(1/x) = m(x)",
    "H_3: alpha != 1",
    "H_4: alpha != -1",
    "not Q: The minimal polynomial of alpha + alpha^-1 over F does NOT have degree n/2"
]

N_HYP = 4
NEG_Q_INDEX = 4