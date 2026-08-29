import sympy
from sympy import Symbol, cyclotomic_poly, Poly, gcd, isprime
from sympy.polys.domains import GF, QQ

# Top-level setup
# No specific named objects required for this domain

def conditions(witness):
    """
    Checks whether the given witness satisfies the hypotheses and fails the conclusion.
    The witness is expected to be a tuple (K, n) where K is either a SymPy domain 
    (like QQ or GF(p)) or an integer representing the characteristic of the field, 
    and n is the index of the cyclotomic polynomial.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            K_obj, n = witness
            if hasattr(K_obj, 'characteristic'):
                p = K_obj.characteristic()
                is_field = K_obj.is_Field
            else:
                p = int(K_obj)
                is_field = isprime(p) or p == 0
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: K is a field such that the characteristic of K does not divide n
    try:
        if not is_field:
            h1 = False
        elif p == 0:
            h1 = (n != 0)
        else:
            h1 = (n % p != 0)
    except Exception:
        h1 = False

    # H_2: Phi_n(x) is the n-th cyclotomic polynomial evaluated over K
    try:
        x = Symbol('x')
        poly = cyclotomic_poly(n, x)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: Phi_n(x) is inseparable over K (meaning it HAS repeated roots)
    try:
        if not h2:
            neg_q = False
        else:
            x = Symbol('x')
            poly = cyclotomic_poly(n, x)
            if p == 0:
                g = gcd(poly, poly.diff(x))
                neg_q = sympy.degree(g, x) > 0
            else:
                poly_gf = Poly(poly, domain=GF(p))
                deriv_gf = poly_gf.diff()
                g = poly_gf.gcd(deriv_gf)
                neg_q = g.degree() > 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field such that the characteristic of K does not divide n",
    "H_2: Phi_n(x) is the n-th cyclotomic polynomial evaluated over K",
    "¬Q: Phi_n(x) is inseparable over K (has repeated roots)"
]

N_HYP = 2
NEG_Q_INDEX = 2