import sympy
from sympy.ntheory import isprime, divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            n = witness.get('n')
        else:
            p, q, n = witness
    except Exception:
        return [False, False, False, False]

    try:
        p_int = int(p)
        h1_ok = bool(p_int % 2 != 0 and isprime(p_int) and p_int == p)
    except Exception:
        h1_ok = False

    try:
        q_int = int(q)
        h2_ok = bool(q_int % 2 != 0 and isprime(q_int) and q_int == q)
    except Exception:
        h2_ok = False

    try:
        n_int = int(n)
        h3_ok = bool(n_int == p * q and n_int == n)
    except Exception:
        h3_ok = False

    try:
        n_int = int(n)
        neg_q_ok = bool(divisor_sigma(n_int) % 4 != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: q is an odd prime number",
    "H_3: n = p q",
    "¬Q: sigma(n) is not divisible by 4"
]

N_HYP = 3
NEG_Q_INDEX = 3