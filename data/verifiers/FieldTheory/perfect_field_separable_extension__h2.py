import sympy
from sympy import Poly, QQ, ZZ, GF
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "Every algebraic extension of a perfect field is separable."
    
    The witness is expected to be a sympy.Poly representing the minimal polynomial
    of a simple algebraic extension E = F(alpha) over the base field F = witness.domain.
    """
    try:
        if not isinstance(witness, Poly):
            witness = Poly(witness)
    except Exception:
        return [False, False, False]

    # H_1: F is a perfect field
    try:
        domain = witness.domain
        h1 = False
        if getattr(domain, 'is_Field', False):
            if domain.characteristic == 0:
                h1 = True
            elif getattr(domain, 'is_FiniteField', False) or type(domain).__name__ in ('FiniteField', 'GaloisField'):
                h1 = True
    except Exception:
        h1 = False

    # H_2: The extension E/F is algebraic
    # A simple extension is algebraic if its minimal polynomial is irreducible and non-constant.
    try:
        h2 = False
        if witness.is_univariate and witness.degree() >= 1:
            if witness.is_irreducible:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The field extension E/F is NOT separable
    # An algebraic extension is inseparable if the minimal polynomial shares a root with its derivative.
    try:
        neg_q = False
        if witness.is_univariate and witness.degree() >= 1:
            deriv = witness.diff()
            if deriv.is_zero:
                neg_q = True
            else:
                g = witness.gcd(deriv)
                if g.degree() > 0:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a perfect field",
    "H_2: The extension E/F is algebraic",
    "¬Q: The field extension E/F is not separable"
]

N_HYP = 2
NEG_Q_INDEX = 2