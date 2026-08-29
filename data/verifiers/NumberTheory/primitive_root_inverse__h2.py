import sympy
from sympy.ntheory import is_primitive_root

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False]
        n, g = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (int(n) == n) and (n > 1)
    except Exception:
        h1 = False

    try:
        h2 = (int(g) == g) and bool(is_primitive_root(g, n))
    except Exception:
        h2 = False

    try:
        if not ((int(g) == g) and (int(n) == n) and (n > 1)):
            neg_q = False
        else:
            try:
                g_inv = sympy.mod_inverse(g, n)
                neg_q = not bool(is_primitive_root(g_inv, n))
            except ValueError:
                # If the modular inverse does not exist, the conclusion fails.
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: g is a primitive root modulo n",
    "¬Q: The modular inverse g^{-1} modulo n is not a primitive root modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2