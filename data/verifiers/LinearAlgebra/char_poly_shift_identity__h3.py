import sympy as sp
from sympy import Matrix, eye, Symbol

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        A, c = witness
    except Exception:
        return [False, False, False]
        
    x = Symbol('x')
    
    # H1: A is an n x n matrix over F
    try:
        h1 = isinstance(A, Matrix) and A.is_square
    except Exception:
        h1 = False
        
    # H2: p_A(x) is the characteristic polynomial of A
    try:
        if h1:
            p_A = A.charpoly(x).as_expr()
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: p_{A+cI_n}(x) != p_A(x - c)
    try:
        if not h1 or not h2:
            return [h1, h2, False]
            
        n = A.shape[0]
        I = eye(n)
        
        try:
            # c * I handles both scalar multiplication and matrix multiplication
            B = A + c * I
            if not isinstance(B, Matrix):
                neg_q = False
                return [h1, h2, neg_q]
            p_B = B.charpoly(x).as_expr()
        except Exception:
            neg_q = False
            return [h1, h2, neg_q]
            
        try:
            p_A_xc = p_A.subs(x, x - c)
            if p_B == p_A_xc or sp.expand(p_B - p_A_xc) == 0:
                neg_q = False
            else:
                neg_q = True
        except Exception:
            # Substitution failed (e.g., x - c is invalid because c is a matrix),
            # meaning p_A(x-c) is not a valid scalar polynomial, so equality fails.
            neg_q = True
            
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over F",
    "H_2: p_A(x) is the characteristic polynomial of A",
    "¬Q: p_{A+cI_n}(x) != p_A(x - c)"
]

N_HYP = 2
NEG_Q_INDEX = 2