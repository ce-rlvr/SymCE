import sympy
from sympy.ntheory import n_order

# No specific named object bindings are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            d = witness.get('d')
        else:
            n, a, d = witness
    except Exception:
        return [False, False, False]

    def is_int(x):
        return (isinstance(x, int) and not isinstance(x, bool)) or isinstance(x, sympy.Integer)

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = is_int(n) and n > 1
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to n
    try:
        h2 = is_int(a) and sympy.gcd(a, n) == 1
    except Exception:
        h2 = False

    # ¬Q: The multiplicative order of a modulo d does NOT divide the multiplicative order of a modulo n
    try:
        if not is_int(d):
            neg_q = False
        else:
            ord_n = n_order(a, n)
            ord_d = n_order(a, d)
            neg_q = (ord_n % ord_d != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer coprime to n",
    "¬Q: The multiplicative order of a modulo d does not divide the multiplicative order of a modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2