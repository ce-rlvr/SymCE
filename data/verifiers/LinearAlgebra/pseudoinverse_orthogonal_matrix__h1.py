import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        Q_pinv = witness.pinv()
        Q_T = witness.T
        diff = Q_pinv - Q_T
        
        if diff.is_zero_matrix is False:
            neg_q = True
        elif diff.is_zero_matrix is True:
            neg_q = False
        else:
            diff = sympy.simplify(diff)
            neg_q = not diff.is_zero_matrix
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Moore-Penrose pseudoinverse Q^+ is not equal to the transpose Q^T"
]

N_HYP = 0
NEG_Q_INDEX = 0