import sympy
from sympy.ntheory import totient

def conditions(witness):
    """
    Given a witness tuple (a, n), checks if it satisfies the hypotheses
    and fails the conclusion of the false Euler's Theorem conjecture.
    """
    try:
        # Witness is expected to be a tuple (a, n)
        if len(witness) != 2:
            return [False, False, False]
        a, n = witness
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1_ok = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1_ok = False

    # H_2: a is an integer
    try:
        h2_ok = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2_ok = False

    # ¬Q: a^{\phi(n)} \not\equiv 1 \pmod n
    try:
        if h1_ok and h2_ok:
            phi_n = int(totient(n))
            # pow(base, exp, mod) is efficient and safe
            neg_q_ok = pow(int(a), phi_n, int(n)) != (1 % int(n))
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer",
    "¬Q: a^{\\phi(n)} \\not\\equiv 1 \\pmod n"
]

N_HYP = 2
NEG_Q_INDEX = 2