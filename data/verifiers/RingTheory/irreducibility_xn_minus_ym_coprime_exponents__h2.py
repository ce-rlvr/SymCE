import sympy
from sympy.polys.domains import QQ, ZZ, FF
import math

# Top-level setup for witness expressions
x, y = sympy.symbols('x y')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (F, n, m)
    where F is a sympy domain (e.g., QQ, FF(2)), and n, m are integers.
    """
    try:
        F, n, m = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H_2: The greatest common divisor of n and m is 1
    try:
        h2 = bool(math.gcd(int(n), int(m)) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: The polynomial x^n - y^m is reducible in F(x,y) (or is not a valid polynomial)
    try:
        n_int = int(n)
        m_int = int(m)
        
        # If exponents are negative, it's a rational function, not a polynomial.
        if n_int < 0 or m_int < 0:
            neg_q = True
        elif n_int == 0 and m_int == 0:
            # x^0 - y^0 = 0, which is not irreducible
            neg_q = True
        else:
            poly_expr = x**n_int - y**m_int
            # factor_list returns (constant, [(factor1, mult1), (factor2, mult2), ...])
            factors = sympy.factor_list(poly_expr, domain=F)
            num_factors = sum(mult for f, mult in factors[1])
            
            # A polynomial is irreducible if it has exactly one non-constant factor with multiplicity 1
            neg_q = bool(num_factors != 1)
    except Exception:
        # If factorization fails or expression is invalid, we consider the conclusion to have failed
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The greatest common divisor of n and m is 1",
    "not Q: The polynomial x^n - y^m is reducible in F"
]

N_HYP = 2
NEG_Q_INDEX = 2