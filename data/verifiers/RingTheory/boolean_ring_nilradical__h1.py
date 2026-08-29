import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    # H_1: x is an element of R
    # We verify this by checking if x supports ring-like multiplication.
    try:
        _ = witness * witness
        h1 = True
    except Exception:
        h1 = False

    # Helper to robustly check if an element is the zero element of its ring
    try:
        zero_ref = witness * 0
    except Exception:
        zero_ref = 0

    def is_zero(val):
        try:
            if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
                return True
        except Exception:
            pass
        try:
            if hasattr(val, 'is_zero') and val.is_zero:
                return True
        except Exception:
            pass
        try:
            if val == 0:
                return True
        except Exception:
            pass
        try:
            if val == zero_ref:
                return True
        except Exception:
            pass
        return False

    # H_2: There exists a positive integer n such that x^n = 0
    h2 = False
    try:
        curr = witness
        # Check powers up to 20 (sufficient for typical small counterexamples like nilpotent matrices)
        for _ in range(1, 21):
            if is_zero(curr):
                h2 = True
                break
            curr = curr * witness
    except Exception:
        h2 = False

    # ¬Q: x != 0 (The conclusion "x = 0" must FAIL)
    try:
        neg_q = not is_zero(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "H_2: There exists a positive integer n such that x^n = 0",
    "¬Q: x != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2