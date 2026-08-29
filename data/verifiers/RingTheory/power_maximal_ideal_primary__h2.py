import sympy
from sympy.ntheory import factorint
from sympy.abc import x, y, z

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, m, n = witness
            elif len(witness) == 2:
                m, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
        
        m = int(m)
        n = int(n)
    except Exception:
        return [False, False, False]

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = (n > 0)
    except Exception:
        h2 = False

    try:
        mn = m ** n
        abs_mn = abs(mn)
        abs_m = abs(m)

        if abs_mn == 1:
            is_primary = False
        elif abs_mn == 0:
            is_primary = True
        else:
            is_primary = len(factorint(abs_mn)) == 1

        if abs_mn == 0:
            rad = 0
        elif abs_mn == 1:
            rad = 1
        else:
            rad = 1
            for p in factorint(abs_mn).keys():
                rad *= p

        is_m_primary = is_primary and (rad == abs_m)
        neg_q = not is_m_primary
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: n is a positive integer",
    "¬Q: M^n is not an M-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2