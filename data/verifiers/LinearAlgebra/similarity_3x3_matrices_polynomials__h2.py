import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_minpoly(M, x):
    try:
        poly_expr = M.minimal_polynomial(x)
        return sympy.Poly(poly_expr, x).as_expr()
    except Exception:
        pass
        
    cp = M.charpoly(x)
    expr = cp.as_expr()
    factors = sympy.factor_list(expr)
    
    powers = [range(1, k+1) for f, k in factors[1]]
    
    best_deg = float('inf')
    best_poly = None
    
    n = M.shape[0]
    Z = zeros(n, n)
    
    for p in itertools.product(*powers):
        test_expr = sympy.Integer(1)
        for (f, _), power in zip(factors[1], p):
            test_expr *= f**power
            
        poly = sympy.Poly(test_expr, x)
        coeffs = poly.all_coeffs()
        
        degree = len(coeffs) - 1
        val = Z
        for i, c in enumerate(coeffs):
            power = degree - i
            val += c * (M ** power)
            
        if val == Z:
            if degree < best_deg:
                best_deg = degree
                best_poly = test_expr
                
    poly = sympy.Poly(best_poly, x)
    lc = poly.LC()
    return sympy.Poly(best_poly / lc, x).as_expr()

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]
        
    # H1: A and B are 3x3 matrices over a field F
    try:
        h1 = isinstance(A, MatrixBase) and A.shape == (3, 3) and \
             isinstance(B, MatrixBase) and B.shape == (3, 3)
    except Exception:
        h1 = False
        
    # H2: A and B have the same minimal polynomial
    try:
        x = sympy.Symbol('x')
        h2 = bool(sympy.expand(get_minpoly(A, x) - get_minpoly(B, x)) == 0)
    except Exception:
        h2 = False
        
    # neg_Q: A and B are NOT similar matrices over F
    # For 3x3 matrices, similarity is equivalent to having the same minimal AND characteristic polynomials.
    try:
        x = sympy.Symbol('x')
        char_diff = sympy.expand(A.charpoly(x).as_expr() - B.charpoly(x).as_expr())
        min_diff = sympy.expand(get_minpoly(A, x) - get_minpoly(B, x))
        neg_q = bool(char_diff != 0 or min_diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are 3x3 matrices over a field F",
    "H_2: A and B have the same minimal polynomial",
    "¬Q: A and B are not similar matrices over F"
]

N_HYP = 2
NEG_Q_INDEX = 2