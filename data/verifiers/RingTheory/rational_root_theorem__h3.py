import sympy
from sympy import Poly, ZZ
from sympy.abc import x

def conditions(witness):
    try:
        if hasattr(witness, 'f') and hasattr(witness, 'p') and hasattr(witness, 'q'):
            f = witness.f
            p = witness.p
            q = witness.q
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            f, p, q = witness
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            f, r = witness
            r_sym = sympy.Rational(r)
            p = r_sym.p
            q = r_sym.q
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H1: f(x) is a polynomial in Z[x]
    try:
        poly = Poly(f, x)
        h1 = poly.domain == ZZ
    except Exception:
        h1 = False

    # H2: a_n != 0 and a_0 != 0
    try:
        poly = Poly(f, x)
        coeffs = poly.all_coeffs()
        a_n = coeffs[0]
        a_0 = coeffs[-1]
        h2 = (a_n != 0) and (a_0 != 0)
    except Exception:
        h2 = False

    # neg_Q: not (p divides a_0 and q divides a_n)
    try:
        poly = Poly(f, x)
        coeffs = poly.all_coeffs()
        a_n = coeffs[0]
        a_0 = coeffs[-1]
        
        if int(p) != p or int(q) != q:
            neg_q = False
        else:
            p = int(p)
            q = int(q)
            
            if p == 0:
                div_p = (a_0 == 0)
            else:
                div_p = (a_0 % p == 0)
                
            if q == 0:
                div_q = (a_n == 0)
            else:
                div_q = (a_n % q == 0)
                
            neg_q = not (div_p and div_q)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: f is a polynomial in Z over x", "H_2: leading and constant coefficients are non-zero", "not Q: p does not divide a_0 or q does not divide a_n"]
N_HYP = 2
NEG_Q_INDEX = 2