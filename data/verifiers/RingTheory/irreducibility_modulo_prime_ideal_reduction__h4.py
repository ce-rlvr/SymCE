import sympy
import functools
from sympy.abc import x

ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: f(x) is a primitive polynomial",
    "H_4: The reduction of f(x) modulo P is irreducible over R/P",
    "¬Q: f(x) is reducible over R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    if not isinstance(witness, (tuple, list)) or len(witness) < 2:
        return [False, False, False, False, False]
    
    p_val = witness[-2]
    f_expr = witness[-1]
    
    if isinstance(f_expr, str):
        try:
            f_expr = sympy.sympify(f_expr)
        except Exception:
            pass

    # H1: R is an integral domain
    # We evaluate in ZZ, which is an integral domain.
    h1 = True
    
    # H2: P is a prime ideal of R
    try:
        p_int = int(p_val)
        h2 = sympy.isprime(p_int)
    except Exception:
        h2 = False
        
    # Determine the variable
    try:
        if hasattr(f_expr, 'free_symbols'):
            symbols = f_expr.free_symbols
            if len(symbols) == 1:
                var = list(symbols)[0]
            else:
                var = x
        else:
            var = x
    except Exception:
        var = x
        
    # H3: f(x) is a primitive polynomial
    try:
        f_poly = sympy.Poly(f_expr, var)
        if not f_poly.domain.is_IntegerRing:
            h3 = False
        else:
            coeffs = f_poly.all_coeffs()
            c_gcd = functools.reduce(sympy.gcd, coeffs)
            h3 = (abs(c_gcd) == 1)
    except Exception:
        h3 = False
        
    # H4: The reduction of f(x) modulo P is irreducible over R/P
    try:
        if h2:
            f_mod_p = sympy.Poly(f_expr, var, modulus=p_int)
            h4 = bool(f_mod_p.is_irreducible)
        else:
            h4 = False
    except Exception:
        h4 = False
        
    # neg_Q: f(x) is reducible over R
    try:
        f_poly_zz = sympy.Poly(f_expr, var, domain='ZZ')
        neg_q = not bool(f_poly_zz.is_irreducible)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]