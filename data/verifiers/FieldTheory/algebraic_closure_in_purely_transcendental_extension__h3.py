import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC
from sympy.abc import x, y, z
from sympy.polys.domains.fractionfield import FractionField
from sympy.polys.domains.polynomialring import PolynomialRing

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a purely transcendental extension of F",
    "¬Q: K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            K = witness.get('K')
        else:
            F, E, K = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: E is a purely transcendental extension of F
    try:
        h2 = False
        if E == F:
            h2 = True
        elif getattr(E, 'is_Field', False):
            d = E
            is_transcendental = True
            while d != F:
                if isinstance(d, FractionField):
                    d = d.domain
                elif isinstance(d, PolynomialRing):
                    d = d.domain
                else:
                    is_transcendental = False
                    break
            if is_transcendental and d == F:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: K is not equal to F
    try:
        neg_q = getattr(K, 'is_Field', False) and (K != F)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]