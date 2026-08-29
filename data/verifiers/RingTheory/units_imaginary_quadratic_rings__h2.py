import sympy
import sympy.ntheory

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    # H_1: d is a square-free integer strictly less than -1
    try:
        is_int = isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer)
        if is_int:
            val = int(witness)
            if val < -1:
                factors = sympy.ntheory.factorint(abs(val))
                h1 = all(v == 1 for v in factors.values())
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: The group of units of R is not exactly {1, -1}
    try:
        is_int = isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer)
        if is_int:
            val = int(witness)
            # For a square-free integer d, the ring of integers of Q(sqrt(d))
            # has units != {1, -1} iff d > 0 (real quadratic) or d in (-1, -3).
            neg_q = bool(val > 0 or val in (-1, -3))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is a square-free integer strictly less than -1",
    "¬Q: The group of units of R is not exactly {1, -1}"
]

N_HYP = 1
NEG_Q_INDEX = 1