import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import GF

def get_char(w):
    try:
        if hasattr(w, 'characteristic'):
            c = w.characteristic
            return c() if callable(c) else c
        if hasattr(w, 'char'):
            c = w.char
            return c() if callable(c) else c
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    try:
        c = get_char(witness)
        if c == 0:
            h1 = True
        elif getattr(witness, 'is_Field', False):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        is_field = getattr(witness, 'is_Field', False)
        if is_field:
            c = get_char(witness)
            if c == 0:
                q = True
            elif hasattr(witness, 'order') and witness.order > 0:
                q = True
            else:
                q = False
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Every irreducible polynomial over F is a separable polynomial",
    "not Q: The field F is not a perfect field"
]

N_HYP = 1
NEG_Q_INDEX = 1