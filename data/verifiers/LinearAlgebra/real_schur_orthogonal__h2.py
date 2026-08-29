import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Q is an n x n real matrix
    try:
        h1 = (isinstance(witness, Matrix) and 
              witness.is_square and 
              witness.shape[0] >= 1 and 
              all(elem.is_real for elem in witness))
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails.
    # The specified block diagonal form is an orthogonal matrix.
    # Since P is orthogonal, P^T Q P = B implies Q = P B P^T.
    # The product of orthogonal matrices is orthogonal, so Q must be orthogonal.
    # Conversely, the true theorem guarantees every real orthogonal matrix can be put into this form.
    # Thus, the conclusion fails if and only if Q is NOT orthogonal.
    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            prod = sympy.simplify(witness.T * witness)
            is_orthogonal = (prod == eye(n))
            neg_q = not is_orthogonal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "¬Q: Q cannot be diagonalized into the specified orthogonal block form (i.e., Q is not orthogonal)"
]

N_HYP = 1
NEG_Q_INDEX = 1