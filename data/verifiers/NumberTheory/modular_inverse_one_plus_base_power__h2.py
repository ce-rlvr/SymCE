import sympy
import math

# Top-level setup
# (No named bindings needed for this number theory domain)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            k = witness.get('k')
        elif hasattr(witness, 'a') and hasattr(witness, 'k'):
            a = witness.a
            k = witness.k
        else:
            a, k = witness
    except Exception:
        return [False, False]

    # H_1: a >= 2 is an integer
    try:
        h1 = (int(a) == a) and (a >= 2)
    except Exception:
        h1 = False

    # neg_Q: The modular inverse of 1+a modulo a^k is NOT congruent to \sum_{i=0}^{k-1} (-a)^i \pmod{a^k}
    try:
        if not (int(k) == k):
            neg_q = True
        else:
            k = int(k)
            if k < 0:
                # Modulus a^k is not an integer, so standard modular arithmetic is undefined
                neg_q = True
            else:
                a_int = int(a)
                modulus = a_int**k
                try:
                    inv = pow(1 + a_int, -1, modulus)
                except ValueError:
                    # 1+a is not invertible modulo a^k
                    neg_q = True
                else:
                    s = sum((-a_int)**i for i in range(k))
                    neg_q = (inv - s) % modulus != 0
    except Exception:
        neg_q = True

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a >= 2 is an integer",
    "¬Q: The modular inverse of 1+a modulo a^k is not congruent to \\sum_{i=0}^{k-1} (-a)^i \\pmod{a^k}"
]

N_HYP = 1
NEG_Q_INDEX = 1