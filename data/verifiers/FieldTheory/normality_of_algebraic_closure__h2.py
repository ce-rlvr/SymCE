import sympy
import sympy.abc
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

def conditions(witness):
    # H_1: K is a field
    try:
        if witness in (sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            h1_ok = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1_ok = True
        elif hasattr(witness, 'is_field') and witness.is_field:
            h1_ok = True
        elif witness in (QQ, RR, CC):
            h1_ok = True
        elif type(witness).__name__ in ('AlgebraicField', 'RationalField', 'RealField', 'ComplexField', 'GaloisField'):
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: \overline{K} is not a normal extension of K
    try:
        # The algebraic closure of any field K is the splitting field of all polynomials over K.
        # By definition, a splitting field is a normal extension.
        # Therefore, the algebraic closure is ALWAYS a normal extension of K.
        # The conclusion is always True, meaning its negation is always False.
        neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "¬Q: \\overline{K} is not a normal extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1