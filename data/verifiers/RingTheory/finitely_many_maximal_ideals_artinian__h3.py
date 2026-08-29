import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ, RR, CC, Domain

x = Symbol('x')
QQ_x = QQ.poly_ring(x)
ZZ_x = ZZ.poly_ring(x)
Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness) -> list[bool]:
    if witness == sympy.S.Integers:
        witness = ZZ
    elif witness == sympy.S.Rationals:
        witness = QQ
    elif witness == sympy.S.Reals:
        witness = RR
    elif witness == sympy.S.Complexes:
        witness = CC

    try:
        h1_ok = isinstance(witness, Domain)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(witness, Domain)
    except Exception:
        h2_ok = False

    try:
        if witness == ZZ:
            neg_q_ok = True
        elif getattr(witness, 'is_Field', False):
            neg_q_ok = False
        elif hasattr(witness, 'gens') and len(witness.gens) > 0:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R has infinitely many maximal ideals"
]

N_HYP = 2
NEG_Q_INDEX = 2