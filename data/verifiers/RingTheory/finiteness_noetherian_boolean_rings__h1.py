import sympy
from sympy import Symbol, S
from sympy.polys.domains import ZZ, QQ, RR, CC, GF

# Top-level setup
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def is_noetherian(ring):
    if ring in (ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
    if getattr(ring, 'is_Field', False):
        return True
    if getattr(ring, 'is_PID', False):
        return True
    if ring.__class__.__name__ == 'PolynomialRing':
        return is_noetherian(ring.domain)
    if ring.__class__.__name__ in ('FractionField', 'AlgebraicField', 'RealField', 'ComplexField', 'FiniteField'):
        return True
    raise ValueError("Cannot determine if ring is Noetherian")

def is_infinite(ring):
    if ring in (ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes):
        return True
    if ring.__class__.__name__ in ('PolynomialRing', 'FractionField', 'AlgebraicField', 'RealField', 'ComplexField'):
        return True
    if ring.__class__.__name__ == 'FiniteField':
        return False
    if getattr(ring, 'is_FiniteField', False):
        return False
    raise ValueError("Cannot determine if ring is infinite")

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_noetherian(witness))
    except Exception:
        h1 = False

    try:
        neg_q = bool(is_infinite(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: R is an infinite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1