import sympy as sp

x, t = sp.symbols('x t')

def is_valid_extension(poly, p):
    """
    Checks if `poly` defines a valid field extension over GF(p)(t).
    It must be an irreducible polynomial in x over GF(p)(t).
    """
    if not sp.isprime(p):
        return False
    try:
        # Ensure all coefficients are integers
        poly_xt = sp.Poly(poly, x, t)
        for c in poly_xt.coeffs():
            if not c.is_integer:
                return False
                
        poly_x = sp.Poly(poly, x)
        deg_x = poly_x.degree()
        if deg_x < 1:
            return False
            
        # Leading coefficient in x must not vanish modulo p
        lc = poly_x.LC()
        lc_poly = sp.Poly(lc, t)
        is_lc_zero = True
        for c in lc_poly.coeffs():
            if c % p != 0:
                is_lc_zero = False
                break
        if is_lc_zero:
            return False
            
        # Check irreducibility modulo p
        factors = sp.factor_list(poly, x, t, modulus=p)
        if len(factors[1]) == 1 and factors[1][0][1] == 1:
            return True
        return False
    except Exception:
        return False

def is_purely_inseparable(poly, p):
    """
    Checks if the extension defined by `poly` is purely inseparable.
    In characteristic p, this means the minimal polynomial is of the form x^(p^n) - c(t) mod p.
    """
    try:
        poly_x = sp.Poly(poly, x)
        deg = poly_x.degree()
        if deg < 1:
            return False
            
        # Degree must be a power of p
        temp = deg
        while temp % p == 0:
            temp = temp // p
        if temp != 1:
            return False
        
        # All intermediate coefficients in x must be 0 modulo p
        coeffs = poly_x.all_coeffs()
        for c in coeffs[1:-1]:
            c_poly = sp.Poly(c, t)
            for cc in c_poly.coeffs():
                if cc % p != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Witness should be a tuple: (p, poly_E, poly_K)
    where p is a prime characteristic,
    poly_E is the minimal polynomial of E over F_p(t),
    poly_K is the minimal polynomial of K over F_p(t).
    """
    try:
        p, poly_E, poly_K = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_valid_extension(poly_E, p)
    except Exception:
        h1 = False
        
    try:
        h2 = is_purely_inseparable(poly_E, p)
    except Exception:
        h2 = False
        
    try:
        k_valid = is_valid_extension(poly_K, p)
        k_pure = is_purely_inseparable(poly_K, p)
        # The conclusion is that K/F is purely inseparable.
        # We want the conclusion to FAIL, so K/F must be a valid extension but NOT purely inseparable.
        neg_q = k_valid and not k_pure
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: The extension E/F is purely inseparable",
    "¬Q: The extension K/F is not purely inseparable"
]

N_HYP = 2
NEG_Q_INDEX = 2