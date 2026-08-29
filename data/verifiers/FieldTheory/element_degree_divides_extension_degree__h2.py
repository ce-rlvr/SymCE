import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup
# The witness can be provided either as a tuple of integers representing the degrees (deg_K, deg_alpha),
# or as a tuple of minimal polynomials (poly_K, poly_alpha) over Q.

CONDITION_LABELS = [
    "H_1: K is a finite field extension of F",
    "¬Q: The degree of F(alpha) over F does not divide the degree of K over F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # First, try to interpret the witness as a tuple of integer degrees
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            if isinstance(witness[0], int) and isinstance(witness[1], int):
                deg_K, deg_alpha = witness
                h1 = (deg_K >= 1 and deg_alpha >= 1)
                neg_q = (deg_K % deg_alpha != 0)
                return [bool(h1), bool(neg_q)]
    except Exception:
        pass

    # Second, try to interpret the witness as a tuple of minimal polynomials over Q
    try:
        poly_K, poly_alpha = witness
        pK = Poly(poly_K, x, domain='QQ')
        pA = Poly(poly_alpha, x, domain='QQ')
        
        h1 = pK.degree() >= 1 and pK.is_irreducible and pA.degree() >= 1 and pA.is_irreducible
        
        deg_K = pK.degree()
        deg_alpha = pA.degree()
        neg_q = (deg_K % deg_alpha != 0)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]