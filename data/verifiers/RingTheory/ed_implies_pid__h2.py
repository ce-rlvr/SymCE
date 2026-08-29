import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a Principal Ideal Domain (PID)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # H_1: R is an integral domain
    try:
        h1 = False
        if getattr(witness, 'is_Ring', False):
            if getattr(witness, 'is_Field', False):
                h1 = True
            elif getattr(witness, 'is_UFD', False):
                h1 = True
            elif hasattr(witness, 'dom') and hasattr(witness, 'gens'):
                dom = witness.dom
                if getattr(dom, 'is_Field', False) or getattr(dom, 'is_UFD', False):
                    h1 = True
            elif witness == ZZ:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: R is NOT a Principal Ideal Domain (PID)
    try:
        if not getattr(witness, 'is_Ring', False):
            neg_q = True
        else:
            neg_q = not getattr(witness, 'is_PID', False)
    except Exception:
        neg_q = True

    return [h1, neg_q]