import math
from sympy.ntheory import isprime

# Top-level setup: no named bindings needed for number theory witnesses.

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        p, k, a = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        p_int = int(p)
        h1 = (p_int == p) and bool(isprime(p_int))
    except Exception:
        h1 = False

    # H_2: k is a positive integer
    try:
        k_int = int(k)
        h2 = (k_int == k) and k_int > 0
    except Exception:
        h2 = False

    # H_3: a is an integer such that gcd(a, p) = 1
    try:
        a_int = int(a)
        p_int = int(p)
        h3 = (a_int == a) and math.gcd(a_int, p_int) == 1
    except Exception:
        h3 = False

    # ¬Q: The congruence x^k \equiv a \pmod p does NOT have exactly gcd(k, p-1) mutually incongruent solutions modulo p
    try:
        p_int = int(p)
        k_int = int(k)
        a_int = int(a)
        expected_solutions = math.gcd(k_int, p_int - 1)
        actual_solutions = sum(1 for x in range(p_int) if pow(x, k_int, p_int) == (a_int % p_int))
        neg_q = actual_solutions != expected_solutions
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k is a positive integer",
    "H_3: a is an integer such that gcd(a, p) = 1",
    "¬Q: The congruence x^k ≡ a (mod p) does not have exactly gcd(k, p-1) solutions modulo p"
]

N_HYP = 3
NEG_Q_INDEX = 3