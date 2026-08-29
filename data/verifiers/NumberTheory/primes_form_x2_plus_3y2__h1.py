import math

# Top-level setup
# (No specific named bindings required for this number theory problem)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str):
            h1 = False
        else:
            p = int(witness)
            if p != witness:
                h1 = False
            else:
                h1 = (p == 3) or (p % 3 == 1)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, str):
            neg_q = False
        else:
            p = int(witness)
            if p != witness:
                neg_q = False
            elif p < 0:
                # Squares and positive multiples of squares cannot sum to a negative number
                neg_q = True
            else:
                found = False
                limit_y = math.isqrt(p // 3)
                for y in range(limit_y + 1):
                    rem = p - 3 * y * y
                    if rem < 0:
                        continue
                    x = math.isqrt(rem)
                    if x * x == rem:
                        found = True
                        break
                neg_q = not found
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p = 3 or p \\equiv 1 \\pmod 3",
    "¬Q: There do not exist integers x and y such that p = x^2 + 3y^2"
]

N_HYP = 1
NEG_Q_INDEX = 1