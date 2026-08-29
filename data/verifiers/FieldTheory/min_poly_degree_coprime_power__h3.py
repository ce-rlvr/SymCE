import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α is algebraic over F",
    "H_3: k is a positive integer such that gcd(k, n) = 1",
    "¬Q: The minimal polynomial of α^k over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness of the form (poly_expr, k), where:
      - poly_expr is a SymPy expression representing the minimal polynomial of α over Q
      - k is the integer power
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        poly_expr, k = witness
        
        free_vars = poly_expr.free_symbols
        if len(free_vars) != 1:
            return [False, False, False, False]
        var = list(free_vars)[0]
        
        # We work over the field of rational numbers (QQ)
        poly = sp.Poly(poly_expr, var, domain='QQ')
        
        # H1: F is a field
        # QQ is a field, so this holds as long as the polynomial is valid over QQ
        h1_ok = poly.domain.is_Field
        
        # H2: α is algebraic over F
        # This means the polynomial must be irreducible over F and have degree >= 1
        n = poly.degree()
        h2_ok = (n >= 1) and poly.is_irreducible
        
        # H3: k is a positive integer such that gcd(k, n) == 1
        try:
            k_int = int(k)
            h3_ok = (k_int > 0) and (math.gcd(k_int, n) == 1)
        except Exception:
            h3_ok = False
            k_int = 1  # Fallback to prevent crashes in the next steps
            
        # ¬Q: The minimal polynomial of α^k over F does NOT have degree n
        # We find the minimal polynomial of α^k by computing the resultant
        # of poly(y) and (var - y^k) with respect to y.
        y = sp.Dummy('y')
        poly_y = poly_expr.subs(var, y)
        
        R = sp.resultant(poly_y, var - y**k_int, y)
        
        # The resultant R(var) has roots (α_i)^k. Since poly is irreducible, 
        # all roots are conjugate, so their k-th powers share the same minimal polynomial.
        # The minimal polynomial is simply the square-free part of R.
        P = sp.sqf_part(R)
        deg_P = sp.degree(P, var)
        
        neg_q_ok = (deg_P != n)
        
        return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False, False]