import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = n > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            has_solution = False
            if n > 0:
                k = 1
                while (k + 1) * (k + 2) <= 2 * n:
                    if (2 * n) % (k + 1) == 0:
                        m = (2 * n) // (k + 1)
                        if (m - k) > 0 and (m - k) % 2 == 0:
                            has_solution = True
                            break
                    k += 1
            neg_q = not has_solution
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The Diophantine equation n = (k+1)(2x+k)/2 has no solution in positive integers x and k"
]

N_HYP = 1
NEG_Q_INDEX = 1