import sympy

def conditions(witness) -> list[bool]:
    m = witness
    try:
        inv = sympy.mod_inverse(m - 1, m)
        q_ok = bool((inv - (m - 1)) % m == 0)
    except Exception:
        q_ok = False

    neg_q = not q_ok
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of m-1 modulo m is not congruent to m-1 (mod m) or is undefined"
]

N_HYP = 0
NEG_Q_INDEX = 0