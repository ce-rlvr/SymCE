import math
import sympy
from sympy import gcd

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        # Check if witness is mathematically an integer greater than 2
        h1 = (n == witness) and (n > 2)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        if (n == witness) and (n > 0):
            prod = 1
            for i in range(1, n):
                if math.gcd(i, n) == 1:
                    prod = (prod * i) % n
            # The conclusion states the product is congruent to 1 (mod n).
            # The negated conclusion is that it is NOT congruent to 1 (mod n).
            neg_q = (prod != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 2",
    "¬Q: The product of all positive integers less than n and coprime to n is not congruent to 1 (mod n)"
]

N_HYP = 1
NEG_Q_INDEX = 1