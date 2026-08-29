import sympy
from sympy.ntheory import divisor_sigma, divisor_count

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            h1 = (n > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        n = int(witness)
        if n <= 0:
            neg_q = False
        else:
            sigma_n = divisor_sigma(n)
            d_n = divisor_count(n)
            
            ineq_holds = (sigma_n <= n * d_n)
            eq_holds = (sigma_n == n * d_n)
            iff_holds = (eq_holds == (n == 1))
            
            q = ineq_holds and iff_holds
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sigma(n) > n * d(n) or equality does not hold iff n = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1