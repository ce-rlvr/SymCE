import sympy
from sympy import Matrix, Symbol, Rational, Poly, minpoly, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: alpha in E is an element with minimal polynomial m(x) over F",
    "¬Q: The field trace Tr_{E/F}(alpha) is NOT equal to -dim(E/F(alpha)) a_{d-1}"
]

def conditions(witness):
    x = Symbol('x')
    
    # H_1: witness represents an element alpha in an algebra E over F with a minimal polynomial
    try:
        if not hasattr(witness, 'is_square'):
            M = Matrix(witness)
        else:
            M = witness
            
        if not M.is_square:
            return [False, False]
            
        m = minpoly(M, x)
        m_poly = Poly(m, x)
        d = m_poly.degree()
        
        if d > 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        return [False, False]
        
    # neg_Q: The trace is NOT equal to -dim(E/F(alpha)) * a_{d-1}
    try:
        if not h1:
            neg_q = False
        else:
            # a_{d-1} is the coefficient of x^{d-1}
            a_d1 = m_poly.nth(d - 1)
            
            # Dimension of E over F is n (size of the matrix)
            n = M.shape[0]
            
            # dim(E/F(alpha)) is the dimension of E divided by the degree of F(alpha) over F
            deg_ext = Rational(n, d)
            
            expected_trace = -deg_ext * a_d1
            actual_trace = M.trace()
            
            neg_q = bool(actual_trace != expected_trace)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]