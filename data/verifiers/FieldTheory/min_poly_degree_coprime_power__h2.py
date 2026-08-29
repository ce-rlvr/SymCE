import sympy
from sympy import Poly, Symbol, resultant
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        F_name, P_expr, k = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field
    try:
        h1 = F_name in ['Q', 'QQ', 'RationalField', 'R', 'C']
    except Exception:
        h1 = False
        
    # H2: The minimal polynomial of α over F has degree n
    try:
        P_expr = sympy.sympify(P_expr)
        symbols = P_expr.free_symbols
        if len(symbols) == 1:
            var = list(symbols)[0]
            P_poly = Poly(P_expr, var, domain='QQ')
            n = P_poly.degree()
            h2 = bool(P_poly.is_irreducible and n >= 1)
        else:
            h2 = False
            n = 0
    except Exception:
        h2 = False
        n = 0
        
    # H3: k is a positive integer such that gcd(k, n) = 1
    try:
        if isinstance(k, (int, sympy.Integer)):
            k_val = int(k)
            h3 = bool((k_val > 0) and (math.gcd(k_val, n) == 1))
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: The minimal polynomial of α^k over F has degree n
    try:
        if not h2:
            neg_q = False
        else:
            var_y = sympy.Symbol('y')
            if var_y == var:
                var_y = sympy.Symbol('z')
            
            # The resultant of P(var) and var_y - var^k with respect to var
            # gives a polynomial in var_y whose roots are the k-th powers of the roots of P.
            R = resultant(P_poly.as_expr(), var_y - var**k_val, var)
            R_poly = Poly(R, var_y, domain='QQ')
            
            # Since P is irreducible over Q, R is a power of the minimal polynomial of α^k.
            factors = R_poly.factor_list()
            if len(factors[1]) == 0:
                deg_minpoly = 0
            else:
                minpoly_alpha_k = factors[1][0][0]
                deg_minpoly = Poly(minpoly_alpha_k, var_y).degree()
                
            neg_q = bool(deg_minpoly != n)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The minimal polynomial of α over F has degree n",
    "H_3: k is a positive integer such that gcd(k, n) = 1",
    "¬Q: The minimal polynomial of α^k over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3