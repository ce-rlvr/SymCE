import sympy
from sympy import Poly, QQ, RR, CC, ZZ
from sympy.abc import x, y, z
from sympy.polys.domains import FractionField, AlgebraicField, PolynomialRing

def conditions(witness) -> list[bool]:
    try:
        F, S, E = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    try:
        if not isinstance(S, (list, set, tuple)):
            h2 = False
        else:
            h2 = True
            for p in S:
                if not isinstance(p, Poly):
                    h2 = False
                    break
                if len(p.gens) != 1:
                    h2 = False
                    break
                if p.domain != F:
                    try:
                        if F.unify(p.domain) != F:
                            h2 = False
                            break
                    except Exception:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    try:
        def is_algebraic_extension(E, F):
            if E == F:
                return True
            if hasattr(E, 'domain') and E.domain == F:
                if isinstance(E, AlgebraicField):
                    return True
                if isinstance(E, (FractionField, PolynomialRing)):
                    return False
            if F == QQ and E in (RR, CC):
                return False
            if isinstance(E, (FractionField, PolynomialRing)):
                try:
                    if E.domain == F or F.unify(E.domain) == E.domain:
                        return False
                except Exception:
                    pass
            return True
            
        neg_q = not is_algebraic_extension(E, F)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS: list[str] = [
    "H_1: F is a field",
    "H_2: S is an arbitrary set of polynomials over F",
    "¬Q: E is not an algebraic extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2