import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: P is a permutation matrix
    h1_ok = False
    try:
        if hasattr(witness, 'shape') and len(witness.shape) == 2:
            rows, cols = witness.shape
            if rows == cols:
                is_perm = True
                for i in range(rows):
                    ones = sum(1 for j in range(cols) if witness[i, j] == 1)
                    zeros_cnt = sum(1 for j in range(cols) if witness[i, j] == 0)
                    if ones != 1 or zeros_cnt != cols - 1:
                        is_perm = False
                        break
                if is_perm:
                    for j in range(cols):
                        ones = sum(1 for i in range(rows) if witness[i, j] == 1)
                        zeros_cnt = sum(1 for i in range(rows) if witness[i, j] == 0)
                        if ones != 1 or zeros_cnt != rows - 1:
                            is_perm = False
                            break
                h1_ok = is_perm
    except Exception:
        h1_ok = False

    # neg_Q: Not all n singular values of P are exactly equal to 1
    neg_q = False
    try:
        if hasattr(witness, 'singular_values') and hasattr(witness, 'shape'):
            svs = witness.singular_values()
            rows = witness.shape[0]
            if len(svs) != rows:
                q = False
            else:
                q = True
                for sv in svs:
                    if sympy.simplify(sv - 1) != 0:
                        q = False
                        break
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: P is a permutation matrix",
    "¬Q: Not all n singular values of P are exactly equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1