import sympy

def conditions(witness) -> list[bool]:
    try:
        p, q = witness
        p = int(p)
        q = int(q)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = bool(sympy.isprime(q))
    except Exception:
        h2 = False

    try:
        sigma_pq = sympy.divisor_sigma(p * q)
        formula = p * q + p + q + 1
        neg_q = bool(sigma_pq != formula)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: q is a prime number",
    "¬Q: sigma(pq) != pq + p + q + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2