import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        # Witness should be a tuple (a, n)
        if len(witness) != 2:
            return [False, False, False]
        a, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            a_int = int(a)
            n_int = int(n)
            phi_n = int(totient(n_int))
            val = pow(a_int, phi_n, n_int)
            neg_q = (val != (1 % n_int))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer",
    "¬Q: a^{\\varphi(n)} \\not\\equiv 1 \\pmod n"
]

N_HYP = 2
NEG_Q_INDEX = 2