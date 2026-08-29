import sympy
import math

def conditions(witness):
    try:
        n = int(witness)
        h1_ok = (n == witness) and (n > 0)
    except Exception:
        h1_ok = False

    try:
        n = int(witness)
        if n <= 0 or n != witness:
            neg_q_ok = False
        else:
            phi_n = sympy.totient(n)
            expected = sympy.totient(phi_n)
            
            count = 0
            if n == 1:
                count = 1
            else:
                for g in range(1, n):
                    if math.gcd(g, n) == 1:
                        if sympy.n_order(g, n) == phi_n:
                            count += 1
            
            neg_q_ok = (count != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The number of distinct primitive roots modulo n is not exactly phi(phi(n))"
]

N_HYP = 1
NEG_Q_INDEX = 1