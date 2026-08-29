import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            q = witness.get('q')
            r = witness.get('r')
        else:
            n, p, q, r = witness
    except Exception:
        return [False] * 5

    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(sympy.isprime(q) and q % 2 != 0)
    except Exception:
        h2 = False

    try:
        h3 = bool(p != q and q != r and p != r)
    except Exception:
        h3 = False

    try:
        h4 = bool(n == p * q * r)
    except Exception:
        h4 = False

    try:
        neg_q = bool(sympy.divisor_sigma(n) % 8 != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: q is an odd prime number",
    "H_3: p, q, and r are pairwise distinct",
    "H_4: n = p * q * r",
    "¬Q: sigma(n) is not divisible by 8"
]

N_HYP = 4
NEG_Q_INDEX = 4