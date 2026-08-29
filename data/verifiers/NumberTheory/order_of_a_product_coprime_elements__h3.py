import math
from sympy.ntheory import n_order

def conditions(witness):
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
        return [False] * 5

    try:
        h1_ok = type(n) is int and n > 1
    except Exception:
        h1_ok = False

    try:
        h2_ok = type(a) is int and type(b) is int and math.gcd(a, n) == 1 and math.gcd(b, n) == 1
    except Exception:
        h2_ok = False

    try:
        h3_ok = type(k) is int and n_order(b, n) == k
    except Exception:
        h3_ok = False

    try:
        h4_ok = type(h) is int and math.gcd(h, k) == 1
    except Exception:
        h4_ok = False

    try:
        neg_q_ok = n_order((a * b) % n, n) != h * k
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a and b are integers coprime to n",
    "H_3: The multiplicative order of b modulo n is k",
    "H_4: gcd(h, k) = 1",
    "¬Q: The multiplicative order of ab modulo n is not equal to hk"
]

N_HYP = 4
NEG_Q_INDEX = 4