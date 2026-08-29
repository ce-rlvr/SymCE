import sympy
from sympy.ntheory import divisors, totient

def conditions(witness):
    try:
        if int(witness) != witness:
            return [False]
        n = int(witness)
        divs = divisors(n)
        tot_sum = sum(totient(d) for d in divs)
        neg_q = bool(tot_sum != n)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{d|n} phi(d) != n"
]

N_HYP = 0
NEG_Q_INDEX = 0