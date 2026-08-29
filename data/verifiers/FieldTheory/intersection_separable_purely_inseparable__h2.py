import sympy
from sympy import cancel, Poly
from sympy.ntheory import isprime
from sympy.abc import x, y

# Top-level setup
# (No special groups or matrices needed for this field theory conjecture)

def check_eq_mod_p(expr1, expr2, p, x_sym):
    """
    Checks if expr1 == expr2 in the field of rational functions GF(p)(x_sym).
    """
    diff = cancel(expr1 - expr2)
    num, den = diff.as_numer_denom()
    
    den_poly = Poly(den, x_sym, domain=sympy.GF(p))
    if den_poly.is_zero:
        return False
        
    num_poly = Poly(num, x_sym, domain=sympy.GF(p))
    return num_poly.is_zero

def rat_deg(expr, p, x_sym):
    """
    Computes the degree of a rational function in GF(p)(x_sym).
    The degree of A(x)/B(x) is max(deg(A), deg(B)) after cancelling common factors mod p.
    """
    num, den = cancel(expr).as_numer_denom()
    num_poly = Poly(num, x_sym, domain=sympy.GF(p))
    den_poly = Poly(den, x_sym, domain=sympy.GF(p))
    
    if den_poly.is_zero:
        raise ValueError("Denominator is zero mod p")
    
    # Cancel common factors modulo p
    gcd_poly = num_poly.gcd(den_poly)
    num_poly = num_poly.quo(gcd_poly)
    den_poly = den_poly.quo(gcd_poly)
    
    d_num = num_poly.degree() if not num_poly.is_zero else -1
    d_den = den_poly.degree() if not den_poly.is_zero else -1
    return max(d_num, d_den)

def conditions(witness):
    """
    Expected witness dictionary structure:
    {
        'p': prime integer (characteristic of the fields),
        'x': sympy symbol for the generator of L = GF(p)(x),
        'y': sympy symbol used for certificates,
        'F_gen': expression in x generating F,
        'E_gen': expression in x generating E,
        'K_gen': expression in x generating K,
        'F_in_E_cert': expression in y such that F_gen == cert(E_gen) mod p,
        'F_in_K_cert': expression in y such that F_gen == cert(K_gen) mod p,
        'K_insep_m': integer m >= 0,
        'K_insep_cert': expression in y such that K_gen**(p**m) == cert(F_gen) mod p,
        'intersect_elem': expression in x representing an element in E \cap K but not in F,
        'intersect_in_E_cert': expression in y such that intersect_elem == cert(E_gen) mod p,
        'intersect_in_K_cert': expression in y such that intersect_elem == cert(K_gen) mod p
    }
    """
    try:
        p = witness['p']
        if not isprime(p):
            return [False, False, False]
            
        x_sym = witness['x']
        y_sym = witness['y']
        F_gen = witness['F_gen']
        E_gen = witness['E_gen']
        K_gen = witness['K_gen']
    except Exception:
        return [False, False, False]
        
    # H_1: E and K are subfields of a common field L containing a base field F
    # Verified by checking that F is a subfield of E and K.
    try:
        cert_F_in_E = witness['F_in_E_cert']
        F_in_E_ok = check_eq_mod_p(F_gen, cert_F_in_E.subs(y_sym, E_gen), p, x_sym)
        
        cert_F_in_K = witness['F_in_K_cert']
        F_in_K_ok = check_eq_mod_p(F_gen, cert_F_in_K.subs(y_sym, K_gen), p, x_sym)
        
        h1_ok = bool(F_in_E_ok and F_in_K_ok)
    except Exception:
        h1_ok = False

    # H_2: K is a purely inseparable extension of F
    # Verified by checking that K_gen**(p**m) is in F for some m >= 0.
    try:
        m = witness['K_insep_m']
        if m < 0:
            h2_ok = False
        else:
            cert_K_insep = witness['K_insep_cert']
            K_pow = K_gen**(p**m)
            h2_ok = bool(check_eq_mod_p(K_pow, cert_K_insep.subs(y_sym, F_gen), p, x_sym))
    except Exception:
        h2_ok = False

    # ¬Q: The intersection E ∩ K is not equal to F
    # Verified by providing an element in E and K, and proving it is not in F.
    try:
        int_elem = witness['intersect_elem']
        cert_int_E = witness['intersect_in_E_cert']
        cert_int_K = witness['intersect_in_K_cert']
        
        int_in_E_ok = check_eq_mod_p(int_elem, cert_int_E.subs(y_sym, E_gen), p, x_sym)
        int_in_K_ok = check_eq_mod_p(int_elem, cert_int_K.subs(y_sym, K_gen), p, x_sym)
        
        d_F = rat_deg(F_gen, p, x_sym)
        d_int = rat_deg(int_elem, p, x_sym)
        
        # By Luroth's theorem, [GF(p)(x) : GF(p)(R)] = deg(R).
        # If int_elem is in GF(p)(F_gen), its degree must be a multiple of deg(F_gen).
        if d_F == 0:
            int_notin_F = (d_int > 0)
        else:
            int_notin_F = (d_int % d_F != 0)
            
        neg_q_ok = bool(int_in_E_ok and int_in_K_ok and int_notin_F)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E and K are subfields of a common field L containing a base field F",
    "H_2: K is a purely inseparable extension of F",
    "¬Q: The intersection E ∩ K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2