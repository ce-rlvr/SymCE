import sympy
from sympy.ntheory import isprime, totient

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(isprime(witness))
    except Exception:
        h1 = False

    try:
        neg_q = bool(totient(witness + 2) != totient(witness) + 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: phi(p+2) != phi(p) + 2"
]

N_HYP = 1
NEG_Q_INDEX = 1