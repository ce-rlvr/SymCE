import sympy
from sympy.ntheory import totient, divisor_sigma

# Top-level setup
# (No named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness) -> list[bool]:
    try:
        n = witness
        h1 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and n >= 1
    except Exception:
        h1 = False

    try:
        if h1:
            sigma_n = divisor_sigma(n)
            phi_n = totient(n)
            neg_q = bool(sigma_n * phi_n >= n**2)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sigma(n) * phi(n) >= n^2"
]

N_HYP = 1
NEG_Q_INDEX = 1