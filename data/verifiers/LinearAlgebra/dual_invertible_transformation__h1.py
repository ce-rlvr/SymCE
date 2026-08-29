import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is an invertible linear transformation",
    "¬Q: The dual transformation T* is not invertible, or (T*)^(-1) != (T^(-1))*"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a SymPy Matrix representing the linear transformation T.
    """
    # H_1: T is an invertible linear transformation
    try:
        if not (hasattr(witness, 'is_Matrix') and witness.is_Matrix and witness.is_square):
            h1 = False
        else:
            det = witness.det()
            if det == 0 or det.is_zero is True:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The dual transformation T*: W* -> V* is invertible, and its inverse satisfies (T*)^(-1) = (T^(-1))*
    # We negate this conclusion (i.e., T* is NOT invertible OR the inverse property fails).
    try:
        if not (hasattr(witness, 'is_Matrix') and witness.is_Matrix and witness.is_square):
            neg_q = False
        else:
            # The dual transformation of a matrix is represented by its transpose
            T_star = witness.T
            det_star = T_star.det()
            
            if det_star == 0 or det_star.is_zero is True:
                q = False
            else:
                inv_T_star = T_star.inv()
                T_inv_star = witness.inv().T
                
                if inv_T_star == T_inv_star:
                    q = True
                else:
                    diff = inv_T_star - T_inv_star
                    if diff.is_zero_matrix:
                        q = True
                    else:
                        diff_simp = sp.simplify(diff)
                        q = (diff_simp.is_zero_matrix is True) or (diff_simp == sp.zeros(witness.rows, witness.cols))
            
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]