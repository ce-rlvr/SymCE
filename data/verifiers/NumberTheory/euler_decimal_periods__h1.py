import sympy
from sympy import Integer

def conditions(witness):
    try:
        # Check if witness is an integer
        if not isinstance(witness, (int, Integer)) or isinstance(witness, bool):
            return [False, False, False]
        p = int(witness)
    except Exception:
        return [False, False, False]

    try:
        h1_ok = (p != 2)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (p != 5)
    except Exception:
        h2_ok = False

    try:
        if p <= 0:
            neg_q_ok = False
        else:
            # Calculate the period length of the repeating decimal expansion of 1/p
            m = p
            while m % 2 == 0:
                m //= 2
            while m % 5 == 0:
                m //= 5
            
            if m == 1:
                # Terminating decimal, period length is effectively 0
                L = 0
            else:
                # The period length is the multiplicative order of 10 modulo m
                L = sympy.n_order(10, m)
            
            # Check if L divides p - 1
            if L == 0:
                divides = (p - 1 == 0)
            else:
                divides = ((p - 1) % L == 0)
                
            neg_q_ok = not divides
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p != 2",
    "H_2: p != 5",
    "¬Q: The period length of the repeating decimal expansion of 1/p is not a divisor of p-1"
]

N_HYP = 2
NEG_Q_INDEX = 2