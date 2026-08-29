import sympy
from sympy.ntheory import totient, divisor_sigma

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p < 1:
            neg_q = False
        else:
            phi_p = totient(p)
            sigma_p = divisor_sigma(p)
            neg_q = bool(phi_p + sigma_p != 2 * p)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: phi(p) + sigma(p) != 2p"
]

N_HYP = 0
NEG_Q_INDEX = 0