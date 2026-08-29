import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x

Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            witness = witness[0]
            
        if isinstance(witness, str):
            w_str = witness.replace(" ", "")
            if w_str in ["Z", "ZZ", "Z[x]", "Q[x]", "R[x]", "C[x]", "k[x]"]:
                neg_q = True
        else:
            if witness == ZZ or witness == S.Integers:
                neg_q = True
            elif witness == QQ or witness in (S.Reals, S.Rationals, S.Complexes):
                neg_q = False
            elif hasattr(witness, 'is_PolynomialRing') and witness.is_PolynomialRing:
                neg_q = True
            elif witness.__class__.__name__ == 'PolynomialRing':
                neg_q = True
            elif hasattr(witness, 'is_Field') and witness.is_Field:
                neg_q = False
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R has infinitely many isomorphism classes of simple right modules"
]

N_HYP = 0
NEG_Q_INDEX = 0