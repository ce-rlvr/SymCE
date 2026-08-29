import sympy
from sympy.polys import CC, QQ, RR, ZZ, GF

Complexes = sympy.S.Complexes
Reals = sympy.S.Reals
Rationals = sympy.S.Rationals
Integers = sympy.S.Integers

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    try:
        if witness in (Complexes, Reals, Rationals, CC, QQ, RR):
            h1 = True
        elif witness in (Integers, ZZ):
            h1 = False
        else:
            h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    # neg_Q: F is an algebraically closed field
    try:
        if witness in (Complexes, CC):
            neg_q = True
        elif witness in (Reals, Rationals, Integers, QQ, RR, ZZ):
            neg_q = False
        elif getattr(witness, 'is_Field', False) and str(witness) == 'CC':
            neg_q = True
        elif getattr(witness, 'is_Field', False) and witness.__class__.__name__ == 'ComplexField':
            neg_q = True
        else:
            neg_q = bool(getattr(witness, 'is_algebraically_closed', False))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: F is an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1