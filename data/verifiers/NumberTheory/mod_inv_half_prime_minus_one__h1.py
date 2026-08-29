import sympy
from sympy import mod_inverse

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p != witness:
            q_holds = False
        elif (p - 1) % 2 != 0:
            q_holds = False
        else:
            val = (p - 1) // 2
            try:
                inv = mod_inverse(val, p)
                q_holds = (inv % p) == ((p - 2) % p)
            except Exception:
                q_holds = False
    except Exception:
        q_holds = False

    neg_q = not q_holds
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of (p-1)/2 modulo p is not congruent to p - 2 (mod p)"
]

N_HYP = 0
NEG_Q_INDEX = 0