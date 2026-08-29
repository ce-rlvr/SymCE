import sympy
import sympy.ntheory

def conditions(witness):
    p, a, k = None, None, None
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            k = witness.get('k')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                p, a = witness
            elif len(witness) == 3:
                p, a, k = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: p is an odd prime
    try:
        h1 = sympy.isprime(p) and (p % 2 != 0)
    except Exception:
        h1 = False

    # H2: a is an integer not divisible by p
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool) and (a % p != 0)
    except Exception:
        h2 = False

    # neg_Q: The order of -a modulo p is NOT exactly 2k
    try:
        if k is None:
            k = sympy.ntheory.n_order(a, p)
        order_minus_a = sympy.ntheory.n_order(-a, p)
        neg_q = order_minus_a != 2 * k
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer not divisible by p",
    "¬Q: The order of -a modulo p is not exactly 2k"
]

N_HYP = 2
NEG_Q_INDEX = 2