import sympy
import math

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            k = witness.get('k')
        else:
            n = witness[0]
            a = witness[1]
            k = witness[2] if len(witness) > 2 else None
    except Exception:
        return [False, False, False, False]

    # H_1: n > 1 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and int(n) > 1
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
    except Exception:
        h2 = False

    # H_3: k is the multiplicative order of a modulo n
    try:
        val_a = int(a)
        val_n = int(n)
        if math.gcd(val_a, val_n) != 1:
            expected_k = 0
        else:
            expected_k = sympy.n_order(val_a, val_n)
        
        if k is None:
            k = expected_k
            h3 = True
        else:
            h3 = (int(k) == expected_k)
    except Exception:
        h3 = False

    # ¬Q: k does not divide phi(n)
    try:
        val_n = int(n)
        val_k = int(k)
        phi_n = int(sympy.totient(val_n))
        if val_k == 0:
            q = (phi_n == 0)
        else:
            q = (phi_n % val_k == 0)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "H_2: a is an integer",
    "H_3: k is the multiplicative order of a modulo n",
    "¬Q: k does not divide phi(n)"
]

N_HYP = 3
NEG_Q_INDEX = 3