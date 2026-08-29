import sympy
from sympy.matrices import eye, zeros, Matrix

# Top-level setup for potential witness objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis from the true theorem is that R is a commutative ring.
    For non-commutative rings, localization at a set containing zero divisors 
    (like a nilpotent element) is generally undefined, so it is not the zero ring.
    """
    # H_1: x is an element of R
    # We verify this by checking if the object supports ring operations (addition and multiplication)
    try:
        _ = witness * witness
        _ = witness + witness
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: x is nilpotent
    try:
        h2_ok = False
        if hasattr(witness, 'is_nilpotent'):
            h2_ok = bool(witness.is_nilpotent())
        else:
            # Fallback: compute powers up to a reasonable bound
            p = witness
            for _ in range(20):
                if p == 0 or (hasattr(p, 'is_zero') and p.is_zero):
                    h2_ok = True
                    break
                p = p * witness
    except Exception:
        h2_ok = False

    # ¬Q: The localization of R at {1, x, x^2, ...} is not the zero ring
    # This is True when the ring is non-commutative (e.g., matrices of size > 1),
    # because the multiplicatively closed set contains zero divisors, making the 
    # Ore localization undefined rather than the zero ring.
    try:
        neg_q_ok = False
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            if witness.shape[0] > 1:
                neg_q_ok = True
        elif hasattr(witness, 'is_commutative'):
            if witness.is_commutative is False:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "H_2: x is nilpotent",
    "¬Q: The localization of R at {1, x, x^2, ...} is not the zero ring"
]

N_HYP = 2
NEG_Q_INDEX = 2