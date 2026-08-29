import sympy
from sympy.ntheory import is_primitive_root

CONDITION_LABELS = [
    "H_1: q is a prime number",
    "H_2: p = 3 (mod 8)",
    "¬Q: 2 is not a primitive root modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    p, q = None, None
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            p, q = witness
        else:
            p = witness
    except Exception:
        pass

    try:
        if p is not None:
            p = int(p)
        if q is not None:
            q = int(q)
    except Exception:
        pass

    try:
        if p is not None and q is None:
            q = (p - 1) // 2
        elif q is not None and p is None:
            p = 2 * q + 1
    except Exception:
        pass

    try:
        h1 = sympy.isprime(q)
    except Exception:
        h1 = False

    try:
        h2 = (p % 8 == 3)
    except Exception:
        h2 = False

    try:
        if p is None or p < 2:
            neg_q = True
        else:
            is_pr = is_primitive_root(2, p)
            neg_q = not bool(is_pr)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]