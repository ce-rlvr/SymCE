import math

def is_int(val):
    if isinstance(val, int):
        return True
    if hasattr(val, 'is_integer'):
        if callable(val.is_integer):
            return val.is_integer()
        return bool(val.is_integer)
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness.get('x')
            p = witness.get('p')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            x, p = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: x is an integer
    try:
        h1 = is_int(x)
    except Exception:
        h1 = False

    # H_2: x \equiv x^{-1} \pmod p
    try:
        if is_int(x) and is_int(p):
            x_int = int(x)
            p_int = int(p)
            if p_int != 0 and math.gcd(x_int, p_int) == 1:
                h2 = (x_int * x_int) % p_int == 1 % p_int
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: x \not\equiv 1 \pmod p and x \not\equiv -1 \pmod p
    try:
        if is_int(x) and is_int(p):
            x_int = int(x)
            p_int = int(p)
            if p_int != 0:
                neg_q = (x_int % p_int != 1 % p_int) and (x_int % p_int != (-1) % p_int)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "H_2: x \\equiv x^{-1} \\pmod p",
    "¬Q: x \\not\\equiv 1 \\pmod p and x \\not\\equiv -1 \\pmod p"
]

N_HYP = 2
NEG_Q_INDEX = 2