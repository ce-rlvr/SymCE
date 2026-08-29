import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = ["H_1: p is a non-constant polynomial", "¬Q: the factor ring is an integral domain but not a field"]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness)
    except Exception:
        return [False, False]

    try:
        h1 = bool(p.is_univariate and p.degree() >= 1)
    except Exception:
        h1 = False

    try:
        domain = p.domain
        if domain.is_Field:
            is_domain = bool(p.is_irreducible)
            is_field = bool(p.is_irreducible)
        elif domain == ZZ:
            # For F = ZZ, ZZ[x]/(p(x)) is an integral domain iff p(x) is irreducible.
            # However, it is never a field for any non-constant polynomial.
            is_domain = bool(p.is_irreducible)
            is_field = False
        else:
            # Fallback for unsupported domains
            is_domain = False
            is_field = False
            
        neg_q = bool(is_domain != is_field)
    except Exception:
        neg_q = False

    return [h1, neg_q]