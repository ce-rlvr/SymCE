import sympy
from sympy.ntheory import factorint

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if witness is ZZ or witness is QQ:
            is_semi = True
        else:
            n = int(witness)
            if n == 0:
                is_semi = True
            elif abs(n) == 1:
                is_semi = True
            else:
                factors = factorint(abs(n))
                is_semi = all(exp == 1 for exp in factors.values())
        neg_q = not is_semi
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a semiprime ring"
]

N_HYP = 0
NEG_Q_INDEX = 0