import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: m_A(x) is the minimal polynomial of A",
    "H_2: A^* is the conjugate transpose of A",
    "¬Q: The minimal polynomial of A^* is not the polynomial whose coefficients are the complex conjugates of the corresponding coefficients of m_A(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # We define x as a real symbol so that when we call .conjugate() on the polynomial,
    # it conjugates the coefficients but leaves the variable x unchanged.
    x = sp.Symbol('x', real=True)
    
    # H_1: m_A(x) is the minimal polynomial of A
    try:
        m_A = witness.minpoly(x)
        h1 = True
    except Exception:
        h1 = False
        
    # H_2: A^* is the conjugate transpose of A
    try:
        A_star = witness.H
        h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomial of A^* is NOT the polynomial whose coefficients are 
    # the complex conjugates of the corresponding coefficients of m_A(x).
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            m_A_star = A_star.minpoly(x)
            expected = sp.expand(m_A.conjugate())
            
            diff = sp.simplify(m_A_star - expected)
            if diff == 0:
                neg_q = False
            else:
                eq_zero = diff.equals(0)
                if eq_zero is None:
                    # If sympy cannot determine equality, we conservatively assume they are not equal
                    neg_q = True
                else:
                    neg_q = not eq_zero
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]