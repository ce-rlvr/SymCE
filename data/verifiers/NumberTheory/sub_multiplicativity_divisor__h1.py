import sympy
from sympy.ntheory import divisor_count

# No specific top-level setup needed for this number theory conjecture.

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple or list of two positive integers (m, n).
    """
    try:
        m, n = witness
    except Exception:
        return [False, False]

    # H_1: m and n are positive integers (domain of the divisor function)
    try:
        h1 = (isinstance(m, (int, sympy.Integer)) and 
              isinstance(n, (int, sympy.Integer)) and 
              m > 0 and n > 0)
    except Exception:
        h1 = False

    # ¬Q: The conclusion \tau(mn) \le \tau(m)\tau(n) FAILS
    # Therefore, we check if \tau(mn) > \tau(m)\tau(n)
    try:
        if h1:
            tau_mn = divisor_count(m * n)
            tau_m = divisor_count(m)
            tau_n = divisor_count(n)
            neg_q = bool(tau_mn > tau_m * tau_n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: tau(mn) > tau(m)tau(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1