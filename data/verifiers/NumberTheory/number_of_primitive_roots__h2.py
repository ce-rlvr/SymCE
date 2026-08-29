import sympy
from sympy.ntheory import totient, n_order
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n > 1) and (n == witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            phi_n = totient(n)
            expected = totient(phi_n)
            
            actual = 0
            for g in range(1, n):
                if math.gcd(g, n) == 1:
                    if n_order(g, n) == phi_n:
                        actual += 1
                        
            neg_q = bool(actual != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "¬Q: The number of incongruent primitive roots modulo n is not equal to phi(phi(n))"
]

N_HYP = 1
NEG_Q_INDEX = 1