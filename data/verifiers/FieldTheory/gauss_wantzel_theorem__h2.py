import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = int(witness) >= 3
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, bool):
            neg_q = False
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            phi_n = int(totient(n))
            is_power_of_2 = (phi_n > 0) and ((phi_n & (phi_n - 1)) == 0)
            neg_q = not is_power_of_2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "¬Q: phi(n) is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1