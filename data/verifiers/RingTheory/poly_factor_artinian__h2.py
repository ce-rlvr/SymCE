import sympy
from sympy import QQ, ZZ
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, f = witness
        elif isinstance(witness, dict) and 'F' in witness and 'f' in witness:
            F = witness['F']
            f = witness['f']
        else:
            F = QQ
            f = witness
    except Exception:
        return [False, False]

    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F in [QQ, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif F.__class__.__name__ == 'GaloisField':
            h1 = True
    except Exception:
        h1 = False

    try:
        f_expr = sympy.sympify(f)
        neg_q = bool(sympy.simplify(f_expr) == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: the factor ring is not an Artinian ring"]
N_HYP = 1
NEG_Q_INDEX = 1