import sympy
from sympy import eye, zeros, Rational, Integer, Matrix
from sympy.abc import x, y, z

# Standard linear algebra objects that might be used as witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: R is a ring (witness supports basic ring operations)
    try:
        _ = witness + witness
        _ = witness * witness
        _ = witness - witness
        h1 = True
    except Exception:
        h1 = False

    # H_2: e is an idempotent element (e^2 = e)
    try:
        if hasattr(witness, 'equals'):
            eq = witness.equals(witness * witness)
            if eq is None:
                h2 = bool(witness * witness == witness)
            else:
                h2 = bool(eq)
        else:
            h2 = bool(witness * witness == witness)
    except Exception:
        h2 = False

    # ¬Q: e != 0
    try:
        zero_elem = witness * 0
        if hasattr(witness, 'equals'):
            is_zero = witness.equals(zero_elem)
            if is_zero is None:
                is_zero = (witness == zero_elem)
            neg_q = not bool(is_zero)
        else:
            neg_q = bool(witness != zero_elem)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring (witness supports ring operations)",
    "H_2: e is an idempotent element (e^2 = e)",
    "¬Q: e != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2