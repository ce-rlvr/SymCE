import sympy
from sympy import MatrixBase, eye

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the conjecture.
    """
    try:
        # H_1: T is a linear operator on V
        # We represent a linear operator on a finite-dimensional space as a square matrix.
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        # H_2: I is the identity operator on V
        # This is a structural property of the space; if T is a valid operator, 
        # the identity operator naturally exists and is well-defined.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            I_mat = eye(witness.shape[0])
            
            # The adjoint T^* could be interpreted as the conjugate transpose (standard for C)
            try:
                expr_H = I_mat + witness.H * witness
                det_H = expr_H.det()
                is_H_zero = (sympy.simplify(det_H) == 0)
            except Exception:
                is_H_zero = False
                
            # The adjoint T^* could also be interpreted as the transpose 
            # (e.g., dual map or adjoint w.r.t a symmetric bilinear form)
            try:
                expr_T = I_mat + witness.T * witness
                det_T = expr_T.det()
                is_T_zero = (sympy.simplify(det_T) == 0)
            except Exception:
                is_T_zero = False
                
            # ¬Q: I + T^*T is not invertible (i.e., its determinant is zero)
            neg_q = is_H_zero or is_T_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: I is the identity operator on V",
    "¬Q: I + T^*T is not invertible"
]

N_HYP = 2
NEG_Q_INDEX = 2