import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Q is an n x n real matrix
    try:
        if not getattr(witness, 'is_square', False):
            h1 = False
        else:
            h1 = bool(all(e.is_real for e in witness))
    except Exception:
        h1 = False

    # H_2: All entries of Q are non-negative
    try:
        if not getattr(witness, 'is_square', False):
            h2 = False
        else:
            h2 = bool(all(e >= 0 for e in witness))
    except Exception:
        h2 = False

    # ¬Q: Q is not a permutation matrix
    try:
        if not getattr(witness, 'is_square', False):
            neg_q = False
        else:
            n = witness.rows
            is_perm = True
            for i in range(n):
                row = list(witness.row(i))
                ones = sum(1 for x in row if x == 1)
                zeros_cnt = sum(1 for x in row if x == 0)
                if ones != 1 or zeros_cnt != n - 1:
                    is_perm = False
                    break
            if is_perm:
                for j in range(n):
                    col = list(witness.col(j))
                    ones = sum(1 for x in col if x == 1)
                    zeros_cnt = sum(1 for x in col if x == 0)
                    if ones != 1 or zeros_cnt != n - 1:
                        is_perm = False
                        break
            neg_q = not is_perm
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "H_2: All entries of Q are non-negative",
    "¬Q: Q is not a permutation matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2