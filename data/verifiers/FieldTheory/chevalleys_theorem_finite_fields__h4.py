import sympy
from sympy.abc import x, y, z, t
import itertools

x1, x2, x3, x4, x5 = sympy.symbols('x1 x2 x3 x4 x5')

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: f is a polynomial in n variables",
    "H_3: The total degree of f is strictly less than n",
    "¬Q: f has fewer than 2 roots in F_q^n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        q, vars, f_expr = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: F_q is a finite field
    try:
        if isinstance(q, (int, sympy.Integer)) and q >= 2:
            q_int = int(q)
            h1 = len(sympy.factorint(q_int)) == 1
        else:
            h1 = False
            q_int = 0
    except Exception:
        h1 = False
        q_int = 0
        
    # H2: f is a polynomial in n variables
    try:
        n = len(vars)
        if n < 1:
            h2 = False
            f_poly = None
        else:
            if sympy.isprime(q_int):
                f_poly = sympy.poly(f_expr, *vars, domain=sympy.GF(q_int))
            else:
                f_poly = sympy.poly(f_expr, *vars)
            h2 = f_poly is not None
    except Exception:
        h2 = False
        f_poly = None
        
    # H3: total degree of f is strictly less than n
    try:
        if h2 and f_poly is not None:
            deg = f_poly.total_degree()
            h3 = bool(deg < n)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: number of roots < 2
    try:
        if h2 and h3:
            if q_int**n > 100000:
                neg_q = False # Prevent TLE
            elif sympy.isprime(q_int):
                roots_count = 0
                for pt in itertools.product(range(q_int), repeat=n):
                    val = f_poly.eval(*pt)
                    try:
                        is_zero = (int(val) == 0)
                    except Exception:
                        is_zero = (val == 0 or val == getattr(f_poly.domain, 'zero', 0))
                    if is_zero:
                        roots_count += 1
                neg_q = bool(roots_count < 2)
            else:
                # For prime powers that are not prime, we only handle constant polynomials easily
                p_char = list(sympy.factorint(q_int).keys())[0]
                if f_poly.is_zero:
                    roots_count = q_int**n
                elif f_poly.is_constant:
                    val = f_poly.LC()
                    if val % p_char == 0:
                        roots_count = q_int**n
                    else:
                        roots_count = 0
                else:
                    neg_q = False
                    roots_count = -1
                
                if roots_count != -1:
                    neg_q = bool(roots_count < 2)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]