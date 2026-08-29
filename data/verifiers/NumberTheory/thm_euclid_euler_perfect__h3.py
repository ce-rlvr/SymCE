import sympy

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            n = int(witness['n'])
        elif hasattr(witness, 'p') and hasattr(witness, 'n'):
            p = int(witness.p)
            n = int(witness.n)
        else:
            p, n = witness
            p = int(p)
            n = int(n)
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: 2^p - 1 is a prime number
    try:
        if p > 10000:  # Prevent hanging on excessively large inputs
            h2 = False
        else:
            h2 = sympy.isprime(2**p - 1)
    except Exception:
        h2 = False

    # ¬Q: sigma(n) != 2n
    try:
        if n <= 0:
            neg_q = True
        else:
            neg_q = sympy.divisor_sigma(n) != 2 * n
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: 2^p - 1 is a prime number",
    "¬Q: sigma(n) != 2n"
]

N_HYP = 2
NEG_Q_INDEX = 2