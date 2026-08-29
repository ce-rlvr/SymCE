import sympy
from sympy.ntheory import isprime, is_primitive_root

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False] * 5
        q, a = witness
    except Exception:
        return [False] * 5

    try:
        q_int = int(q)
        h1 = bool(q_int == q and q_int % 2 != 0 and isprime(q_int))
    except Exception:
        h1 = False

    try:
        q_int = int(q)
        p = 2 * q_int + 1
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        h3 = bool(int(a) == a)
    except Exception:
        h3 = False

    try:
        a_int = int(a)
        q_int = int(q)
        p = 2 * q_int + 1
        h4 = bool((a_int % p) != (p - 1))
    except Exception:
        h4 = False

    try:
        a_int = int(a)
        q_int = int(q)
        p = 2 * q_int + 1
        lhs = bool(is_primitive_root(a_int, p))
        rhs = bool(pow(a_int, q_int, p) != 1)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: q is an odd prime",
    "H_2: p = 2q + 1 is a prime number",
    "H_3: a is an integer",
    "H_4: a is not congruent to -1 mod p",
    "¬Q: (a is a primitive root mod p) is not equivalent to (a^q != 1 mod p)"
]

N_HYP = 4
NEG_Q_INDEX = 4