import sympy
from sympy.ntheory import n_order, reduced_totient

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        n, a = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(n, int) and n > 1
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(a, int)
    except Exception:
        h2_ok = False

    try:
        if not (isinstance(n, int) and n > 1 and isinstance(a, int)):
            neg_q_ok = False
        else:
            lam = reduced_totient(n)
            try:
                ord_a = n_order(a, n)
                neg_q_ok = (lam % ord_a != 0)
            except ValueError:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "H_2: a is an integer",
    "¬Q: The multiplicative order of a modulo n does not divide lambda(n) (or is undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2