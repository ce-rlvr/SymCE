import sympy
from sympy import Symbol

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = bool(witness > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The degree of the field extension Q(zeta_n) over Q is not equal to phi(n)
    try:
        if isinstance(witness, bool) or not isinstance(witness, (int, sympy.Integer)):
            neg_q = False
        else:
            n = int(witness)
            if n <= 0:
                neg_q = False
            else:
                x = Symbol('x')
                poly = sympy.cyclotomic_poly(n, x)
                deg = sympy.degree(poly)
                phi_n = sympy.totient(n)
                neg_q = bool(deg != phi_n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The degree of the field extension Q(zeta_n) over Q is not equal to phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1