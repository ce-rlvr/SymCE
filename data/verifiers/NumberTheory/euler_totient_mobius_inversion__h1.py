import sympy
from sympy.ntheory import totient, mobius, divisors

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Witness must be an integer
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            return [False, False]
        n = int(witness)
    except Exception:
        return [False, False]

    # H_1: n >= 1
    try:
        h1 = bool(n >= 1)
    except Exception:
        h1 = False

    # ¬Q: phi(n) != sum_{d|n} mu(d) n/d
    try:
        if n < 1:
            neg_q = False
        else:
            phi_n = totient(n)
            rhs = sum(mobius(d) * (n // d) for d in divisors(n))
            neg_q = bool(phi_n != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "¬Q: phi(n) != sum_{d|n} mu(d) n/d"
]

N_HYP = 1
NEG_Q_INDEX = 1