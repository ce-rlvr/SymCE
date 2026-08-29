import sympy
from sympy import ZZ, QQ, RR, CC

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: Quotient ring of polynomials over R by polynomials over I is not isomorphic to polynomials over R mod I"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = ZZ
            I = witness
    except Exception:
        return [False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R in (ZZ, QQ, RR, CC):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif isinstance(R, (list, set, tuple)):
            h1 = True
            for a in R:
                for b in R:
                    if a * b != b * a:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # neg_Q: I is not an ideal of R
    try:
        is_id = True
        if R in (ZZ, QQ, RR, CC):
            if isinstance(I, (int, sympy.Integer)):
                is_id = True
            elif I in (ZZ, QQ, RR, CC):
                if R == I:
                    is_id = True
                else:
                    is_id = False
            elif isinstance(I, (set, list, tuple)):
                if set(I) == {0}:
                    is_id = True
                else:
                    is_id = False
            else:
                is_id = False
        elif isinstance(R, (list, set, tuple)) and isinstance(I, (list, set, tuple)):
            I_set = set(I)
            for i in I_set:
                for r in R:
                    if (i * r) not in I_set:
                        is_id = False
                for j in I_set:
                    if (i - j) not in I_set:
                        is_id = False
        elif hasattr(I, 'is_ideal'):
            is_id = bool(I.is_ideal)
        else:
            is_id = False

        neg_q = not is_id
    except Exception:
        neg_q = False

    return [h1, neg_q]