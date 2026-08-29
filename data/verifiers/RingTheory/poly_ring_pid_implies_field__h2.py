import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import GF
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    # Map SymPy sets to their corresponding domains if provided
    try:
        if witness == sympy.S.Integers:
            witness = sympy.ZZ
        elif witness == sympy.S.Rationals:
            witness = sympy.QQ
        elif witness == sympy.S.Reals:
            witness = sympy.RR
        elif witness == sympy.S.Complexes:
            witness = sympy.CC
    except Exception:
        pass

    # H_1: R is a commutative ring with identity
    try:
        from sympy.polys.domains.domain import Domain
        from sympy.polys.rings import PolynomialRing
        
        # In SymPy, all polys.domains.Domain and polys.rings.PolynomialRing 
        # instances are commutative rings with identity.
        h1 = isinstance(witness, (Domain, PolynomialRing))
        if not h1 and hasattr(witness, 'is_Field'):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: R is not a field
    try:
        from sympy.polys.rings import PolynomialRing
        if hasattr(witness, 'is_Field'):
            is_f = bool(witness.is_Field)
        elif isinstance(witness, PolynomialRing):
            is_f = False
        else:
            is_f = False
        neg_q = not is_f
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1