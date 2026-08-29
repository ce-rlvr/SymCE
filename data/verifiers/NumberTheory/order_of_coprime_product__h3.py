import sympy
from sympy.ntheory import n_order
from math import gcd

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

CONDITION_LABELS = [
    "H_1: n > 1 is an integer",
    "H_2: a and b are integers",
    "H_3: h is the multiplicative order of a modulo n",
    "H_4: k is the multiplicative order of b modulo n",
    "H_5: gcd(h, k) = 1",
    "¬Q: The multiplicative order of ab modulo n is not hk"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            b = witness.get('b')
            h = witness.get('h')
            k = witness.get('k')
        else:
            n, a, b, h, k = witness
    except Exception:
        return [False] * 6

    # H_1: n > 1 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 1
    except Exception:
        h1 = False

    # H_2: a and b are integers
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h2 = False

    # H_3: h is the multiplicative order of a modulo n
    try:
        h3 = bool(h == n_order(a, n))
    except Exception:
        h3 = False

    # H_4: k is the multiplicative order of b modulo n
    try:
        h4 = bool(k == n_order(b, n))
    except Exception:
        h4 = False

    # H_5: \gcd(h, k) = 1
    try:
        h5 = bool(gcd(int(h), int(k)) == 1)
    except Exception:
        h5 = False

    # ¬Q: The multiplicative order of ab modulo n is not hk
    try:
        neg_q = bool(n_order(a * b, n) != h * k)
    except ValueError:
        # If n_order raises ValueError, ab is not coprime to n,
        # so it has no multiplicative order. Thus it is not hk.
        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]