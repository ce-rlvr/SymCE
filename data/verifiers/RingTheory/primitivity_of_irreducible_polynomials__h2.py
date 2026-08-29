import sympy
from sympy import Poly
from sympy.abc import x, y, z

# Top-level setup
# Variables for polynomial rings
# R is implicitly defined by the domain of the witness polynomial.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "If R is a UFD and f is a polynomial of degree >= 1, then f is primitive."
    (The dropped hypothesis is that f must be irreducible).
    """
    try:
        if not isinstance(witness, Poly):
            f = Poly(witness)
        else:
            f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(f.domain.is_UFD)
    except Exception:
        h1 = False
        
    # H_2: The degree of f is greater than or equal to 1
    try:
        h2 = bool(f.degree() >= 1)
    except Exception:
        h2 = False
        
    # ¬Q: f is not a primitive polynomial
    try:
        cont = f.content()
        if hasattr(f.domain, 'is_unit'):
            is_prim = bool(f.domain.is_unit(cont))
        else:
            # Fallback if is_unit is not available on the domain
            if f.domain.is_Field:
                is_prim = (cont != f.domain.zero)
            else:
                is_prim = (abs(cont) == 1)
        neg_q = not is_prim
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The degree of f is greater than or equal to 1",
    "¬Q: f is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2