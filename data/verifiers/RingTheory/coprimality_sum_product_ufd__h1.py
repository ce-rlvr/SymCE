import sympy as sp
from sympy.abc import x, y, z

def get_gcd(a, b):
    """
    Helper to compute the greatest common divisor.
    Attempts to use a custom .gcd() method if provided by the witness ring elements,
    otherwise falls back to sympy's symbolic gcd.
    """
    if hasattr(a, 'gcd'):
        try:
            return a.gcd(b)
        except Exception:
            pass
            
    sa = sp.sympify(a)
    if hasattr(sa, 'as_expr'):
        sa = sa.as_expr()
        
    sb = sp.sympify(b)
    if hasattr(sb, 'as_expr'):
        sb = sb.as_expr()
        
    return sp.gcd(sp.expand(sa), sp.expand(sb))

def conditions(witness):
    try:
        # The witness should be a pair of elements (a, b) from the ring R
        if len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        # H_1: Let a and b be non-zero elements of R.
        h1 = (a != 0) and (b != 0)
    except Exception:
        h1 = False
        
    try:
        # H_2: The greatest common divisor of a and b is 1.
        g_ab = get_gcd(a, b)
        if hasattr(g_ab, 'as_expr'):
            g_ab = g_ab.as_expr()
        h2 = (g_ab == 1) or (g_ab == -1)
    except Exception:
        h2 = False
        
    try:
        # ¬Q: The greatest common divisor of a+b and ab is NOT 1.
        sum_ab = a + b
        prod_ab = a * b
        g_sum_prod = get_gcd(sum_ab, prod_ab)
        if hasattr(g_sum_prod, 'as_expr'):
            g_sum_prod = g_sum_prod.as_expr()
        neg_q = (g_sum_prod != 1) and (g_sum_prod != -1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "H_2: The greatest common divisor of a and b is 1",
    "¬Q: The greatest common divisor of a+b and ab is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2