import sympy
from sympy.ntheory import n_order

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            n = witness.get('n')
        else:
            a, n = witness
    except Exception:
        return [False, False]

    # H_1: a is an integer strictly greater than 1
    try:
        h1 = (isinstance(a, int) or (isinstance(a, float) and a.is_integer()) or isinstance(a, sympy.Integer)) and a > 1
    except Exception:
        h1 = False

    # neg_Q: The multiplicative order of a modulo a^n + 1 is not exactly 2n
    try:
        m = a**n + 1
        try:
            is_int = (int(m) == m)
        except Exception:
            is_int = False
            
        if not is_int:
            neg_q = True
        elif m <= 1:
            neg_q = True
        else:
            m = int(m)
            try:
                order = n_order(int(a), m)
                neg_q = (order != 2 * n)
            except ValueError:
                # gcd(a, m) != 1, so order is undefined
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer strictly greater than 1",
    "¬Q: The multiplicative order of a modulo a^n + 1 is not exactly 2n"
]

N_HYP = 1
NEG_Q_INDEX = 1