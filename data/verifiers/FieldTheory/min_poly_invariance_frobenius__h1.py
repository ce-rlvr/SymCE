import sympy
from sympy import Poly, symbols, QQ, GF, Matrix

# Top-level setup
# No specific named objects are required for this field theory verifier.

def poly_pow_mod(base, exp, mod_poly, domain):
    gen = mod_poly.gen
    res = Poly(1, gen, domain=domain)
    base = base.rem(mod_poly)
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base).rem(mod_poly)
        base = (base * base).rem(mod_poly)
        exp //= 2
    return res

def get_minpoly_of_power(coeffs, q, p):
    gen = symbols('x')
    if p == 0:
        domain = QQ
    else:
        domain = GF(p)
    
    f = Poly(coeffs, gen, domain=domain)
    d = f.degree()
    if d < 1:
        return None
        
    base = Poly(gen, gen, domain=domain)
    xq = poly_pow_mod(base, q, f, domain)
    
    M_rows = []
    for i in range(d):
        xi = Poly(gen**i, gen, domain=domain)
        xi_xq = (xq * xi).rem(f)
        c = xi_xq.all_coeffs()
        c = [domain.zero] * (d - len(c)) + c
        c.reverse()
        M_rows.append(c)
    
    M = Matrix(M_rows)
    lam = symbols('lam')
    charpoly = M.charpoly(lam)
    
    charpoly_poly = Poly(charpoly.as_expr(), lam, domain=domain)
    factors = charpoly_poly.factor_list()
    
    if not factors[1]:
        return None
        
    min_poly = factors[1][0][0].monic()
    return min_poly

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'p': characteristic of the base field (0 for QQ, or a prime for GF(p))
      'q': the exponent in alpha^q
      'coeffs': list of coefficients of the minimal polynomial of alpha over the base field
    """
    try:
        p = witness['p']
        q = witness['q']
        coeffs = witness['coeffs']
    except Exception:
        return [False, False]
    
    if not isinstance(p, int) or not isinstance(q, int) or not isinstance(coeffs, list):
        return [False, False]
        
    if q < 0:
        return [False, False]
        
    try:
        gen = symbols('x')
        if p == 0:
            domain = QQ
        else:
            domain = GF(p)
        f = Poly(coeffs, gen, domain=domain)
        h1 = f.is_irreducible and f.degree() >= 1
    except Exception:
        h1 = False
        
    try:
        gen = symbols('x')
        if p == 0:
            domain = QQ
        else:
            domain = GF(p)
        f = Poly(coeffs, gen, domain=domain).monic()
        min_poly_q = get_minpoly_of_power(coeffs, q, p)
        if min_poly_q is None:
            neg_q = False
        else:
            # Compare coefficient lists to avoid generator symbol mismatch
            neg_q = (min_poly_q.all_coeffs() != f.all_coeffs())
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is an element of an algebraic extension of the base field",
    "¬Q: The minimal polynomial of alpha^q over the base field is different from the minimal polynomial of alpha"
]

N_HYP = 1
NEG_Q_INDEX = 1