import sympy
from sympy import Symbol, S
from sympy.polys.domains import ZZ, QQ, FF, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
Z = ZZ
Q = QQ
Z_x = ZZ.poly_ring(x)
F2 = FF(2)
F2_x = FF(2).poly_ring(x)

def is_ring(domain):
    try:
        if hasattr(domain, 'is_Ring') and domain.is_Ring:
            return True
        if hasattr(domain, 'is_Field') and domain.is_Field:
            return True
    except Exception:
        pass
    return False

def has_finite_units(domain):
    try:
        if domain == ZZ:
            return True
        if hasattr(domain, 'is_FiniteField') and domain.is_FiniteField:
            return True
        if hasattr(domain, 'is_PolynomialRing') and domain.is_PolynomialRing:
            return has_finite_units(domain.domain)
        if domain == QQ or getattr(domain, 'is_RationalField', False):
            return False
        if getattr(domain, 'is_RealField', False) or getattr(domain, 'is_ComplexField', False):
            return False
        if hasattr(domain, 'is_AlgebraicField') and domain.is_AlgebraicField:
            return False
    except Exception:
        pass
    return False

def is_finite_ring(domain):
    try:
        if hasattr(domain, 'is_FiniteField') and domain.is_FiniteField:
            return True
        if domain == ZZ:
            return False
        if hasattr(domain, 'is_PolynomialRing') and domain.is_PolynomialRing:
            return False
        if domain == QQ or getattr(domain, 'is_RationalField', False):
            return False
        if getattr(domain, 'is_RealField', False) or getattr(domain, 'is_ComplexField', False):
            return False
        if hasattr(domain, 'is_AlgebraicField') and domain.is_AlgebraicField:
            return False
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # Normalize common SymPy sets to their corresponding domains
    try:
        if witness == S.Integers:
            witness = ZZ
        elif witness == S.Rationals:
            witness = QQ
        elif witness == S.Reals:
            witness = RR
        elif witness == S.Complexes:
            witness = CC
    except Exception:
        pass

    try:
        h1_ok = bool(is_ring(witness) and has_finite_units(witness))
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = bool(is_ring(witness) and not is_finite_ring(witness))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The group of units of R is finite",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1