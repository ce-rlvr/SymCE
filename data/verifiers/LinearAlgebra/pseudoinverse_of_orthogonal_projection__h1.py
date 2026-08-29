import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not getattr(witness, 'is_square', False):
            h1 = False
        else:
            diff_proj = witness * witness - witness
            diff_orth = witness - witness.H
            h1 = (diff_proj.is_zero_matrix == True) and (diff_orth.is_zero_matrix == True)
            if not h1:
                h1 = (sympy.simplify(diff_proj).is_zero_matrix == True) and (sympy.simplify(diff_orth).is_zero_matrix == True)
    except Exception:
        h1 = False

    try:
        if not hasattr(witness, 'pinv'):
            neg_q = False
        else:
            pinv_P = witness.pinv()
            if pinv_P.shape != witness.shape:
                neg_q = True
            else:
                diff = pinv_P - witness
                is_eq = (diff.is_zero_matrix == True)
                if not is_eq:
                    is_eq = (sympy.simplify(diff).is_zero_matrix == True)
                neg_q = not is_eq
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an orthogonal projection operator on V",
    "¬Q: The Moore-Penrose pseudoinverse of P is not equal to P"
]

N_HYP = 1
NEG_Q_INDEX = 1