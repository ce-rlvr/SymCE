import sympy
from sympy.ntheory import totient, divisor_sigma

# Top-level setup
# No named bindings needed for number theory

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        n = int(witness)
        neg_q = bool(totient(n) * divisor_sigma(n) >= n**2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: phi(n) * sigma(n) >= n^2"
]

N_HYP = 1
NEG_Q_INDEX = 1