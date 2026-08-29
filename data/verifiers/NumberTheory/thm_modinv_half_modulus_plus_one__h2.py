import sympy
from sympy import mod_inverse

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            h1_ok = False
        else:
            m = int(witness)
            h1_ok = (m % 2 != 0)
    except Exception:
        h1_ok = False

    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            neg_q_ok = False
        else:
            m = int(witness)
            try:
                inv = mod_inverse((m + 1) // 2, m)
                q = (inv == 2)
            except Exception:
                q = False
            neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: m is an odd integer",
    "¬Q: The modular inverse of (m+1)/2 modulo m is not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1