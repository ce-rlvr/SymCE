import sympy
from sympy import Poly, symbols

# Top-level setup for witness expressions
x, y, z, t = symbols('x y z t')

def get_p_and_poly(witness):
    """
    Extracts the characteristic p and the minimal polynomial from the witness.
    The witness can be a dict, a tuple, or just a sympy Poly.
    """
    if isinstance(witness, dict):
        p = witness.get('p', None)
        poly = witness.get('min_poly', witness.get('poly', None))
        if p is None and poly is not None:
            if hasattr(poly, 'domain'):
                if poly.domain.is_QQ or poly.domain.is_ZZ:
                    p = 0
                elif hasattr(poly.domain, 'char'):
                    p = poly.domain.char
        return p, poly
    elif isinstance(witness, sympy.Poly):
        poly = witness
        p = 0
        if hasattr(poly, 'domain'):
            if poly.domain.is_QQ or poly.domain.is_ZZ:
                p = 0
            elif hasattr(poly.domain, 'char'):
                p = poly.domain.char
        return p, poly
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            if isinstance(witness[0], int):
                return witness[0], witness[1]
            elif isinstance(witness[1], int):
                return witness[1], witness[0]
    return None, None

def conditions(witness) -> list[bool]:
    try:
        p, poly = get_p_and_poly(witness)
    except Exception:
        return [False, False, False]
        
    if p is None or poly is None:
        return [False, False, False]
        
    try:
        if not isinstance(poly, sympy.Poly):
            poly = sympy.Poly(poly)
    except Exception:
        return [False, False, False]

    # H_1: F \subseteq K is a field extension
    # We verify this by checking if the provided polynomial is a valid irreducible monic polynomial.
    try:
        if p != 0 and not sympy.isprime(p):
            h1 = False
        else:
            if p == 0:
                h1 = poly.is_irreducible and poly.LC() == 1
            else:
                poly_fp = poly.set_domain(sympy.GF(p))
                h1 = poly_fp.is_irreducible and poly_fp.LC() == 1
    except Exception:
        h1 = False

    # H_2: \alpha \in K is purely inseparable over F
    # An element is purely inseparable iff its minimal polynomial has only one distinct root.
    # In char 0, this means the degree must be 1.
    # In char p > 0, this means the polynomial must be of the form x^{p^e} - a.
    try:
        if p == 0:
            h2 = (poly.degree() == 1)
        else:
            d = poly.degree()
            e = 0
            while p**e < d:
                e += 1
            if p**e != d:
                h2 = False
            else:
                coeffs = poly.all_coeffs()
                if coeffs[0] % p != 1 % p:
                    h2 = False
                else:
                    h2 = True
                    for c in coeffs[1:-1]:
                        if c % p != 0:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of \alpha over F is NOT of the form x^{p^e} - a
    # If p = 0, the characteristic is not a prime, so it cannot be of the form x^{p^e} - a where p is prime.
    try:
        if p == 0:
            neg_q = True
        else:
            d = poly.degree()
            e = 0
            while p**e < d:
                e += 1
            if p**e != d:
                neg_q = True
            else:
                coeffs = poly.all_coeffs()
                if coeffs[0] % p != 1 % p:
                    neg_q = True
                else:
                    neg_q = False
                    for c in coeffs[1:-1]:
                        if c % p != 0:
                            neg_q = True
                            break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F \\subseteq K is a field extension",
    "H_2: \\alpha \\in K is purely inseparable over F",
    "¬Q: The minimal polynomial of \\alpha over F is not of the form x^{p^e} - a"
]

N_HYP = 2
NEG_Q_INDEX = 2