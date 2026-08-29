import sympy

x = sympy.Symbol('x')

def check_mod_p(poly_Q, poly_GFp, p):
    try:
        for c in poly_Q.coeffs():
            if sympy.Rational(c).q % p == 0:
                return False
        
        dict_mod = {}
        for deg_tuple, c in poly_Q.terms():
            c_rat = sympy.Rational(c)
            num = c_rat.p
            den = c_rat.q
            den_inv = sympy.mod_inverse(den, p)
            c_mod = (num * den_inv) % p
            if c_mod != 0:
                dict_mod[deg_tuple] = c_mod
                
        poly_Q_mod = sympy.Poly(dict_mod, x, domain=sympy.GF(p))
        return poly_Q_mod == poly_GFp
    except Exception:
        return False

def conditions(witness):
    """
    Expects a witness representing the local ring R = Z_{(p)}.
    Format can be a dict: {'p': prime, 'f': f_expr, 'g0': g0_expr, 'h0': h0_expr}
    or a tuple: (p, f_expr, g0_expr, h0_expr)
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            f_expr = witness['f']
            g0_expr = witness['g0']
            h0_expr = witness['h0']
        else:
            p, f_expr, g0_expr, h0_expr = witness
    except Exception:
        return [False] * 5

    # H_1: R is a commutative Noetherian ring
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: R is a local ring with maximal ideal m and residue field k = R/m
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # H_3: f is a monic polynomial over R
    try:
        f_poly = sympy.Poly(f_expr, x)
        h3 = f_poly.is_monic
        if h3:
            for c in f_poly.coeffs():
                c_rat = sympy.Rational(c)
                if c_rat.q % p == 0:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H_4: The reduction f_bar factors as g_0 h_0 with g_0, h_0 monic and coprime
    try:
        g0_poly = sympy.Poly(g0_expr, x, domain=sympy.GF(p))
        h0_poly = sympy.Poly(h0_expr, x, domain=sympy.GF(p))
        
        h4 = g0_poly.is_monic and h0_poly.is_monic
        if h4:
            dict_mod = {}
            for deg_tuple, c in f_poly.terms():
                c_rat = sympy.Rational(c)
                num = c_rat.p
                den = c_rat.q
                den_inv = sympy.mod_inverse(den, p)
                c_mod = (num * den_inv) % p
                if c_mod != 0:
                    dict_mod[deg_tuple] = c_mod
            f_bar = sympy.Poly(dict_mod, x, domain=sympy.GF(p))
            
            if f_bar != g0_poly * h0_poly:
                h4 = False
            else:
                gcd_poly = g0_poly.gcd(h0_poly)
                if gcd_poly.degree() != 0:
                    h4 = False
    except Exception:
        h4 = False

    # neg_Q: There do not exist monic polynomials g, h over R such that f = g h lifting the factorization
    try:
        f_Q = sympy.Poly(f_expr, x, domain=sympy.QQ)
        lead, fac_list = f_Q.factor_list()
        divisors = [sympy.Poly(1, x, domain=sympy.QQ)]
        for fac, mult in fac_list:
            fac_monic = fac.monic()
            new_divisors = []
            for d in divisors:
                for i in range(mult + 1):
                    new_divisors.append(d * (fac_monic ** i))
            divisors = new_divisors
            
        neg_q = True
        for g in divisors:
            h = f_Q.exquo(g)
            if check_mod_p(g, g0_poly, p) and check_mod_p(h, h0_poly, p):
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_3: f is a monic polynomial over R",
    "H_4: The reduction f_bar factors as g_0 h_0 with g_0, h_0 monic and coprime",
    "not Q: There do not exist monic polynomials g, h over R such that f = g h lifting the factorization"
]

N_HYP = 4
NEG_Q_INDEX = 4