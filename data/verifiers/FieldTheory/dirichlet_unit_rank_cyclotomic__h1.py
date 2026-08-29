import sympy
from sympy.ntheory import totient

# Top-level setup
# (No named bindings needed for this domain; integers are used directly)

def conditions(witness) -> list[bool]:
    # H_1: n is a positive integer
    try:
        if type(witness) is bool:
            h1 = False
        elif not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n >= 1)
    except Exception:
        h1 = False

    # ¬Q: The unit rank of Q(zeta_n) is not exactly phi(n)/2 - 1
    try:
        n = int(witness)
        # The unit rank of a number field is r1 + r2 - 1.
        # For Q(zeta_n), if n in (1, 2), the field is Q, so r1 = 1, r2 = 0, rank = 0.
        # If n > 2, the field is totally complex of degree phi(n), so r1 = 0, r2 = phi(n)/2, rank = phi(n)/2 - 1.
        if n in (1, 2):
            actual_rank = 0
        else:
            actual_rank = totient(n) // 2 - 1
            
        formula_rank = totient(n) / 2 - 1
        
        neg_q = float(actual_rank) != float(formula_rank)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The unit rank of Q(zeta_n) is not exactly phi(n)/2 - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1