import sympy
from sympy.matrices import MatrixBase, eye, zeros
from sympy import simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: Q is a 3x3 real matrix
    try:
        h1_ok = isinstance(witness, MatrixBase) and witness.shape == (3, 3) and all(e.is_real for e in witness)
    except Exception:
        h1_ok = False

    # H2: Q is an orthogonal matrix
    try:
        diff = witness.T * witness - eye(3)
        h2_ok = all(simplify(e) == 0 for e in diff)
    except Exception:
        h2_ok = False

    # ¬Q: Q does not have an eigenvalue equal to 1
    try:
        det_val = (witness - eye(3)).det()
        neg_q_ok = simplify(det_val) != 0
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: Q is a 3x3 real matrix",
    "H_2: Q is an orthogonal matrix",
    "¬Q: Q does not have an eigenvalue equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2