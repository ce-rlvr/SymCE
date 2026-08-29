import sympy
from sympy.abc import x
from sympy.ntheory import totient

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 1)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (int, sympy.Integer)):
            neg_q = False
        else:
            n = int(witness)
            if n < 1:
                neg_q = False
            else:
                poly = sympy.cyclotomic_poly(n, x)
                deg = totient(n)
                norm = ((-1)**deg) * poly.subs(x, 0)
                neg_q = (norm != 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: The field norm N_{Q(zeta_n)/Q}(zeta_n) is not equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1