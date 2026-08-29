import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: P is an idempotent matrix (P^2 = P)
    try:
        if not isinstance(witness, Matrix):
            h1_ok = False
        elif witness.shape[0] != witness.shape[1]:
            h1_ok = False
        else:
            h1_ok = bool(witness**2 == witness)
    except Exception:
        h1_ok = False

    # H_2: The rank of P is exactly n-1
    try:
        if not isinstance(witness, Matrix) or witness.shape[0] != witness.shape[1]:
            h2_ok = False
        else:
            n = witness.shape[0]
            h2_ok = bool(witness.rank() == n - 1)
    except Exception:
        h2_ok = False

    # neg_Q: The adjugate matrix adj(P) is NOT an idempotent matrix
    try:
        if not isinstance(witness, Matrix) or witness.shape[0] != witness.shape[1]:
            neg_q_ok = False
        else:
            adj_P = witness.adjugate()
            neg_q_ok = not bool(adj_P**2 == adj_P)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is an idempotent matrix (P^2 = P)",
    "H_2: The rank of P is exactly n-1",
    "¬Q: The adjugate matrix adj(P) is not an idempotent matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2