import sympy
from sympy.ntheory import isprime, is_primitive_root

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = int(witness['a'])
            p = int(witness['p'])
            q = int(witness['q'])
        else:
            a, p, q = witness
            a = int(a)
            p = int(p)
            q = int(q)
    except Exception:
        return [False, False, False]

    # H_1: a is a primitive root modulo p
    try:
        if p <= 1:
            h1 = False
        else:
            h1 = bool(is_primitive_root(a, p))
    except Exception:
        h1 = False

    # H_2: q is a prime number that divides p-1
    try:
        h2 = bool(isprime(q) and (p - 1) % q == 0)
    except Exception:
        h2 = False

    # ¬Q: There exists an integer x such that x^q ≡ a (mod p)
    try:
        neg_q = False
        if 1 < p <= 1000000:
            a_mod = a % p
            for x in range(p):
                if pow(x, q, p) == a_mod:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is a primitive root modulo p",
    "H_2: q is a prime number that divides p-1",
    "¬Q: There exists an integer x such that x^q ≡ a (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2