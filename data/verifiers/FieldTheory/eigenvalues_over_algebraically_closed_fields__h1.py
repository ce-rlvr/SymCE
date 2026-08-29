import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square and witness.rows >= 1
    except Exception:
        h1 = False

    try:
        h2 = h1 and all(e.is_real for e in witness)
    except Exception:
        h2 = False

    try:
        if not h2:
            neg_q = False
        else:
            is_rational_matrix = all(e.is_rational for e in witness)
            evs = witness.eigenvals()
            has_eigenvalue_in_K = False
            for ev in evs:
                if is_rational_matrix:
                    if ev.is_rational:
                        has_eigenvalue_in_K = True
                        break
                else:
                    if ev.is_real:
                        has_eigenvalue_in_K = True
                        break
            neg_q = not has_eigenvalue_in_K
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional non-zero vector space over K (witness is a square matrix of size >= 1)",
    "H_2: T: V -> V is a linear transformation (witness has real entries)",
    "¬Q: T has no eigenvalues in K"
]

N_HYP = 2
NEG_Q_INDEX = 2