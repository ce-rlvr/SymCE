import sympy
from sympy import Poly, expand, ZZ, QQ
from sympy.abc import x

def in_domain(c, D):
    try:
        D.from_sympy(c)
        return True
    except Exception:
        return False

def is_poly_in_domain(expr, D):
    try:
        p = Poly(expr, x)
        return all(in_domain(c, D) for c in p.coeffs())
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness tuple (R, F, f, G, H), checks the hypotheses and the negated conclusion.
    R: SymPy domain (e.g. ZZ)
    F: SymPy domain (e.g. QQ)
    f, G, H: SymPy expressions (polynomials in x)
    """
    try:
        R, F, f, G, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # H_2: F is the field of fractions of R
    try:
        h2 = (F == R.get_field())
    except Exception:
        h2 = False
        
    # H_3: G and H are polynomials over F such that f = GH
    try:
        h3 = is_poly_in_domain(G, F) and is_poly_in_domain(H, F) and (expand(f - G * H) == 0)
    except Exception:
        h3 = False
        
    # neg_Q: There do not exist g and h over R and non-zero a and b in F such that G = ag and H = bh and f = gh
    # This conclusion holds if and only if f is a polynomial over R.
    # Therefore the conclusion fails (neg_Q is True) iff f is NOT a polynomial over R.
    try:
        neg_q = not is_poly_in_domain(f, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: G and H are polynomials over F such that f = GH",
    "not Q: There do not exist g and h over R and non-zero a and b in F such that G = ag and H = bh and f = gh"
]

N_HYP = 3
NEG_Q_INDEX = 3