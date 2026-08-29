import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x

ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
RR_x = RR.poly_ring(x)
CC_x = CC.poly_ring(x)

def conditions(witness):
    try:
        if witness == sympy.S.Integers:
            witness = ZZ
        elif witness == sympy.S.Rationals:
            witness = QQ
        elif witness == sympy.S.Reals:
            witness = RR
        elif witness == sympy.S.Complexes:
            witness = CC
    except Exception:
        pass

    try:
        h1 = False
        if witness in [ZZ, QQ, RR, CC, ZZ_x, QQ_x, RR_x, CC_x]:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif hasattr(witness, 'is_PID') and witness.is_PID:
            h1 = True
        elif hasattr(witness, 'get_field'):
            h1 = True
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = sympy.isprime(witness)
    except Exception:
        h1 = False

    try:
        is_local = False
        if witness in [QQ, RR, CC]:
            is_local = True
        elif witness in [ZZ, ZZ_x, QQ_x, RR_x, CC_x]:
            is_local = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            is_local = True
        elif isinstance(witness, (int, sympy.Integer)):
            if witness <= 1:
                is_local = False
            else:
                factors = sympy.factorint(witness)
                is_local = (len(factors) == 1)
        else:
            is_local = False
            
        neg_q = not is_local
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1