import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

Z_ring = ZZ
Q_ring = QQ
R_ring = RR
C_ring = CC

def conditions(witness):
    try:
        h1 = False
        if witness in [ZZ, QQ, RR, CC, sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
        elif hasattr(witness, 'is_commutative') and witness.is_commutative and hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
    except Exception:
        h1 = False

    try:
        is_art = False
        if witness in [QQ, RR, CC, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            is_art = True
        elif witness in [ZZ, sympy.S.Integers]:
            is_art = False
        elif getattr(witness, 'is_Field', False):
            is_art = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            is_art = False
        elif witness.__class__.__name__ == 'FiniteField':
            is_art = True
        elif hasattr(witness, 'is_finite') and witness.is_finite:
            is_art = True
        else:
            is_art = False
        
        neg_q = not is_art
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: R is not isomorphic to a finite direct product of local Artinian rings"
]

N_HYP = 1
NEG_Q_INDEX = 1