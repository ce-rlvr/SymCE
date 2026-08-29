import sympy
from sympy import Symbol, Poly, cancel, fraction, factor_list, diff, isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard groups and matrices
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_fractional_linear(expr, t, p):
    """Check if expr is of the form (at+b)/(ct+d) with ad-bc != 0 mod p."""
    expr = cancel(expr)
    num, den = fraction(expr)
    try:
        num_p = Poly(num, t)
        den_p = Poly(den, t)
    except Exception:
        return False
        
    def degree_mod_p(poly):
        deg = poly.degree()
        while deg >= 0:
            if poly.nth(deg) % p != 0:
                return deg
            deg -= 1
        return -1

    if degree_mod_p(num_p) > 1 or degree_mod_p(den_p) > 1:
        return False
        
    a = num_p.nth(1)
    b = num_p.nth(0)
    c = den_p.nth(1)
    d = den_p.nth(0)
    det = (a*d - b*c) % p
    return det != 0

def is_zero_mod_p(expr, vars, p):
    """Check if a rational expression is identically zero modulo p."""
    expr = cancel(expr)
    num, den = fraction(expr)
    try:
        num_p = Poly(num, *vars)
        for c in num_p.coeffs():
            if c % p != 0:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Witness must be a dictionary containing:
      'p': prime characteristic
      't': Symbol for the transcendental generator of L = F_p(t)
      'X': Symbol for the polynomial variable
      'Y': Symbol representing the generator of K
      'K_gen': rational function in t generating K over F_p
      'sigma_t': rational function in t representing sigma(t)
      'alpha': rational function in t representing the element alpha
      'min_poly': minimal polynomial of sigma(alpha) over K, given as an expression in X and Y
    """
    try:
        p = int(witness['p'])
        if not isprime(p):
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        t = witness['t']
        X = witness['X']
        Y = witness['Y']
        K_gen = witness['K_gen']
        sigma_t = witness['sigma_t']
        alpha = witness['alpha']
        min_poly = witness['min_poly']
    except Exception:
        return [False, False, False]

    # H_1: L/K is a field extension
    # We verify this by checking that K_gen is a non-constant rational function in t.
    # This ensures K = F_p(K_gen) is a valid subfield of L = F_p(t).
    try:
        h1 = bool(t in K_gen.free_symbols)
    except Exception:
        h1 = False

    # H_2: sigma is a K-automorphism of L
    try:
        is_auto = is_fractional_linear(sigma_t, t, p)
        K_gen_sigma = K_gen.subs(t, sigma_t)
        fixes_K = is_zero_mod_p(K_gen_sigma - K_gen, [t], p)
        h2 = bool(is_auto and fixes_K)
    except Exception:
        h2 = False

    # neg_Q: sigma(alpha) is NOT separable over K
    try:
        beta = alpha.subs(t, sigma_t)
        
        # Check that min_poly is irreducible over F_p(Y)
        facs = factor_list(min_poly, modulus=p)
        is_irred = (len(facs[1]) == 1 and facs[1][0][1] == 1)
        
        # Check that min_poly has degree >= 1 in X mod p
        poly_X = Poly(min_poly, X)
        deg_X_mod_p = -1
        for d in range(poly_X.degree(), -1, -1):
            coeff = poly_X.nth(d)
            if not is_zero_mod_p(coeff, [Y], p):
                deg_X_mod_p = d
                break
        
        # Check that beta is a root of min_poly
        eval_poly = min_poly.subs({X: beta, Y: K_gen})
        is_root = is_zero_mod_p(eval_poly, [t], p)
        
        # Check that the formal derivative of min_poly with respect to X is 0 mod p
        deriv = diff(min_poly, X)
        deriv_zero = is_zero_mod_p(deriv, [X, Y], p)
        
        neg_q = bool(is_irred and (deg_X_mod_p >= 1) and is_root and deriv_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: sigma is a K-automorphism of L",
    "not Q: sigma(alpha) is NOT separable over K"
]

N_HYP = 2
NEG_Q_INDEX = 2