import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: e^2 = e
    try:
        h1_ok = bool(witness * witness == witness)
    except Exception:
        h1_ok = False

    # ¬Q: e != 0 and e != 1
    try:
        is_zero = False
        if hasattr(witness, 'is_zero_matrix') and witness.is_zero_matrix:
            is_zero = True
        else:
            try:
                is_zero = bool(witness == 0 * witness)
            except Exception:
                is_zero = bool(witness == 0)
    except Exception:
        is_zero = False

    try:
        is_one = False
        if hasattr(witness, 'is_Identity') and witness.is_Identity:
            is_one = True
        else:
            try:
                is_one = bool(witness == witness**0)
            except Exception:
                is_one = bool(witness == 1)
    except Exception:
        is_one = False

    try:
        neg_q_ok = not is_zero and not is_one
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: e is an element such that e^2 = e",
    "¬Q: e != 0 and e != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1