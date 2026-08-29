import sympy as sp
from sympy.polys.polytools import Poly
from sympy.ntheory import factorint

x = sp.Symbol('x')

def is_prime_power(n):
    if not isinstance(n, int) or n < 2:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (q, d, mod_poly, alpha_poly)
    where:
      - q is the size of the base field F_q (must be a prime power).
      - d is the degree of the extension field.
      - mod_poly is an irreducible polynomial of degree d over F_q.
      - alpha_poly represents the element alpha in the extension field.
    """
    try:
        q, d, mod_poly, alpha_poly = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: q is a prime power
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    # H2: mod_poly is irreducible over F_q of degree d
    try:
        if h1:
            if isinstance(mod_poly, Poly):
                mod_expr = mod_poly.as_expr()
            else:
                mod_expr = mod_poly
            mod_p = Poly(mod_expr, x, domain=sp.GF(q))
            h2 = mod_p.is_irreducible and mod_p.degree() == d and d >= 1
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: alpha_poly is a valid element in the extension field
    try:
        if h1 and h2:
            if isinstance(alpha_poly, Poly):
                alpha_expr = alpha_poly.as_expr()
            else:
                alpha_expr = alpha_poly
            alpha_p = Poly(alpha_expr, x, domain=sp.GF(q))
            alpha_p = alpha_p % mod_p
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: The minimal polynomial of alpha over F_q is NOT given by the product \prod_{i=0}^{d-1} (y - alpha^{q^i})
    # The product has degree d. The minimal polynomial has degree k, where k is the smallest positive integer
    # such that alpha^{q^k} == alpha. The conclusion fails if and only if k < d.
    try:
        if h1 and h2 and h3:
            k = 1
            curr = alpha_p
            
            def poly_pow_mod(base, exp, mod):
                res = Poly(1, x, domain=sp.GF(q))
                b = base
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * b) % mod
                    b = (b * b) % mod
                    exp //= 2
                return res
            
            curr = poly_pow_mod(curr, q, mod_p)
            while curr != alpha_p and k <= d:
                k += 1
                curr = poly_pow_mod(curr, q, mod_p)
            
            neg_q = (k != d)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: q is a prime power",
    "H_2: mod_poly is an irreducible polynomial over F_q of degree d",
    "H_3: alpha is an element of the extension field",
    "¬Q: The minimal polynomial of alpha over F_q is NOT given by the product of (x - alpha^{q^i}) for i from 0 to d-1"
]

N_HYP = 3
NEG_Q_INDEX = 3