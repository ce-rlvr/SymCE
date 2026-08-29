import math

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        c = int(c)
    except Exception:
        return [False, False]

    try:
        h1 = (math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h1 = False

    try:
        q = (math.gcd(a, b) == 1) and (math.gcd(b, c) == 1) and (math.gcd(a, c) == 1)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(a, b, c) = 1",
    "¬Q: a, b, and c are not pairwise coprime"
]

N_HYP = 1
NEG_Q_INDEX = 1