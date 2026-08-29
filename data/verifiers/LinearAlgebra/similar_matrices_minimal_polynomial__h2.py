import sympy
import sympy.matrices
import itertools

# Top-level setup: named object bindings that the witness expression may reference
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_minpoly(M, x):
    """
    Helper function to compute the minimal polynomial of a matrix.
    Tries the built-in method first, then falls back to a robust manual computation
    by checking divisors of the characteristic polynomial.
    """
    try:
        return M.minimal_polynomial(x)
    except Exception:
        pass
    
    n = M.shape[0]
    cp = M.charpoly(x)
    factors = sympy.factor_list(cp.as_expr())[1]
    
    possible_mults = [list(range(1, mult + 1)) for f, mult in factors]
    
    best_poly = cp.as_expr()
    best_deg = n + 1
    
    for mults in itertools.product(*possible_mults):
        poly_expr = sympy.Integer(1)
        for (f, _), m in zip(factors, mults):
            poly_expr *= f**m
        poly_expr = sympy.expand(poly_expr)
        poly = sympy.Poly(poly_expr, x)
        coeffs = poly.all_coeffs()
        
        mat_val = sympy.zeros(n, n)
        deg = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            mat_val += c * (M ** (deg - i))
            
        is_zero = True
        for val in mat_val:
            if sympy.simplify(val) != 0:
                is_zero = False
                break
                
        if is_zero:
            if deg < best_deg:
                best_deg = deg
                best_poly = poly_expr
                
    return sympy.expand(best_poly)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]
        
    # H_1: A and B are n x n matrices over a field F
    try:
        h1 = bool(hasattr(A, 'is_square') and hasattr(B, 'is_square') and 
                  A.is_square and B.is_square and 
                  A.shape == B.shape and
                  hasattr(A, 'charpoly') and hasattr(B, 'charpoly'))
    except Exception:
        h1 = False
        
    # ¬Q: The minimal polynomial of A is NOT equal to the minimal polynomial of B
    try:
        if h1:
            x = sympy.Symbol('x')
            minpoly_A = get_minpoly(A, x)
            minpoly_B = get_minpoly(B, x)
            neg_q = bool(sympy.simplify(minpoly_A - minpoly_B) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices over a field F",
    "¬Q: The minimal polynomial of A is NOT equal to the minimal polynomial of B"
]

N_HYP = 1
NEG_Q_INDEX = 1