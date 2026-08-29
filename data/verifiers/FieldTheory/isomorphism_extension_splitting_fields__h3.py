import sympy
from sympy import Poly, Symbol, roots, QQ
from sympy.polys.numberfields import primitive_element

x = Symbol('x')

def conditions(witness):
    try:
        F = witness.F
        F_prime = witness.F_prime
        phi = witness.phi
        f = witness.f
        f_prime = witness.f_prime
        E = witness.E
        E_prime = witness.E_prime
    except Exception:
        return [False] * 6
        
    # H1: F and F_prime are fields
    try:
        h1 = F.is_Field and F_prime.is_Field
    except Exception:
        h1 = False
        
    # H2: phi is a field isomorphism from F onto F_prime
    try:
        if F == QQ and F_prime == QQ:
            h2 = (phi(QQ(0)) == QQ(0) and 
                  phi(QQ(1)) == QQ(1) and 
                  phi(QQ(1, 2)) == QQ(1, 2))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: f_prime is the polynomial over F_prime whose coefficients are the images of f under phi
    try:
        poly_f = Poly(f, x)
        coeffs_f = poly_f.all_coeffs()
        
        poly_f_prime = Poly(f_prime, x)
        coeffs_f_prime = poly_f_prime.all_coeffs()
        
        if len(coeffs_f) == len(coeffs_f_prime):
            h3 = True
            for c, cp in zip(coeffs_f, coeffs_f_prime):
                if phi(c) != cp:
                    h3 = False
                    break
            if F_prime == QQ:
                for cp in coeffs_f_prime:
                    if cp not in QQ:
                        h3 = False
                        break
        else:
            h3 = False
    except Exception:
        h3 = False

    # Precompute degrees of splitting fields over QQ
    try:
        f_roots_dict = roots(f, x)
        if sum(f_roots_dict.values()) == Poly(f, x).degree():
            f_roots = list(f_roots_dict.keys())
            if len(f_roots) > 0:
                _, min_poly = primitive_element(f_roots, x, ex=True)
                deg_E = min_poly.degree()
            else:
                deg_E = 1
        else:
            deg_E = -1
    except Exception:
        deg_E = -1

    try:
        f_prime_roots_dict = roots(f_prime, x)
        if sum(f_prime_roots_dict.values()) == Poly(f_prime, x).degree():
            f_prime_roots = list(f_prime_roots_dict.keys())
            if len(f_prime_roots) > 0:
                _, min_poly_prime = primitive_element(f_prime_roots, x, ex=True)
                deg_E_prime = min_poly_prime.degree()
            else:
                deg_E_prime = 1
        else:
            deg_E_prime = -2
    except Exception:
        deg_E_prime = -2
        
    # H4: E is a splitting field of f over F
    try:
        h4 = (getattr(E, 'is_Field', False) or E == "SplittingField") and (getattr(witness, 'E_deg', deg_E) == deg_E) and deg_E > 0
    except Exception:
        h4 = False
        
    # H5: E_prime is a splitting field of f_prime over F_prime
    try:
        h5 = (getattr(E_prime, 'is_Field', False) or E_prime == "SplittingField") and (getattr(witness, 'E_prime_deg', deg_E_prime) == deg_E_prime) and deg_E_prime > 0
    except Exception:
        h5 = False
        
    # ¬Q: There does not exist a field isomorphism tau from E onto E_prime extending phi
    try:
        neg_q = (deg_E > 0 and deg_E_prime > 0 and deg_E != deg_E_prime)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F and F_prime are fields",
    "H_2: phi is a field isomorphism from F onto F_prime",
    "H_3: f_prime is the polynomial over F_prime whose coefficients are the images of f under phi",
    "H_4: E is a splitting field of f over F",
    "H_5: E_prime is a splitting field of f_prime over F_prime",
    "¬Q: There does not exist a field isomorphism tau from E onto E_prime extending phi"
]

N_HYP = 5
NEG_Q_INDEX = 5