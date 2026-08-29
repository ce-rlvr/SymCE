import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        pinv_U = witness.pinv()
        adj_U = witness.adjoint()
        neg_q = bool(pinv_U != adj_U)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Moore-Penrose pseudoinverse of U is not equal to the conjugate transpose of U"
]

N_HYP = 0
NEG_Q_INDEX = 0