import sympy
from sympy.ntheory import divisors

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            n_sq = n**2
            if n_sq == 0:
                has_sol = True
            else:
                has_sol = False
                divs = divisors(n_sq)
                for x in divs:
                    y = n_sq // x
                    if x < y and (x % 2) == (y % 2):
                        has_sol = True
                        break
            neg_q = not has_sol
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: There do not exist positive integers b and c such that n^2 + b^2 = c^2"
]

N_HYP = 1
NEG_Q_INDEX = 1