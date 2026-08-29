import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a real symmetric n x n matrix
    try:
        if not hasattr(witness, 'is_symmetric'):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        elif witness.rows == 0:
            h1 = False
        elif not witness.is_symmetric():
            h1 = False
        else:
            h1 = all(e.is_real for e in witness)
    except Exception:
        h1 = False

    # neg_Q: det(A) > prod(a_{ii})
    try:
        det_A = witness.det()
        prod_diag = 1
        for i in range(witness.rows):
            prod_diag *= witness[i, i]
        neg_q = bool(det_A > prod_diag)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a real symmetric n x n matrix",
    "¬Q: det(A) > product of diagonal entries"
]

N_HYP = 1
NEG_Q_INDEX = 1