import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
Z = ZZ
Q = QQ
Z_ring = ZZ
Q_field = QQ

def conditions(witness) -> list[bool]:
    # H_1: R is a ring
    try:
        if witness == S.Integers:
            h1 = True
        elif witness in (S.Reals, S.Rationals, S.Complexes):
            h1 = True
        else:
            name = witness.__class__.__name__
            h1 = 'Ring' in name or 'Field' in name or hasattr(witness, 'is_ring')
    except Exception:
        h1 = False

    # ¬Q: R/J(R) is not a semisimple ring
    try:
        if witness == S.Integers:
            neg_q = True
        elif witness in (S.Reals, S.Rationals, S.Complexes):
            neg_q = False
        else:
            name = witness.__class__.__name__
            if 'Field' in name:
                # Fields have J(R) = 0, R/0 = R is a field, hence semisimple.
                neg_q = False
            elif 'IntegerRing' in name:
                # ZZ has J(ZZ) = 0, ZZ/0 = ZZ is not Artinian, hence not semisimple.
                neg_q = True
            elif 'PolynomialRing' in name:
                # K[x] has J(K[x]) = 0, K[x]/0 = K[x] is not Artinian, hence not semisimple.
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: R/J(R) is not a semisimple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1