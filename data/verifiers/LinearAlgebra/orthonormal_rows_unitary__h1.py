import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'is_Matrix') or not witness.is_Matrix:
            return [False, False]
        
        # H_1: U is a unitary matrix.
        # Since the squareness hypothesis was dropped, we check if U is an isometry (U^H U = I)
        # or a co-isometry (U U^H = I), which are the standard generalizations of unitary matrices.
        I_cols = eye(witness.cols)
        diff_1 = (witness.H * witness) - I_cols
        if diff_1.is_zero_matrix:
            is_isometry = True
        else:
            is_isometry = bool(diff_1.applyfunc(sympy.simplify).is_zero_matrix)
            
        I_rows = eye(witness.rows)
        diff_2 = (witness * witness.H) - I_rows
        if diff_2.is_zero_matrix:
            is_coisometry = True
        else:
            is_coisometry = bool(diff_2.applyfunc(sympy.simplify).is_zero_matrix)
            
        h1 = is_isometry or is_coisometry
    except Exception:
        h1 = False

    try:
        if not hasattr(witness, 'is_Matrix') or not witness.is_Matrix:
            neg_q = False
        else:
            # ¬Q: The rows of U do NOT form an orthonormal basis for C^n.
            # The rows form an orthonormal basis iff they are orthonormal (U U^H = I) 
            # and there are exactly n of them (rows == cols, since rows are vectors in C^n where n = cols).
            I_rows = eye(witness.rows)
            diff_2 = (witness * witness.H) - I_rows
            if diff_2.is_zero_matrix:
                is_ortho = True
            else:
                is_ortho = bool(diff_2.applyfunc(sympy.simplify).is_zero_matrix)
                
            is_basis = is_ortho and (witness.rows == witness.cols)
            neg_q = not is_basis
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The rows of U do not form an orthonormal basis for C^n"
]

N_HYP = 1
NEG_Q_INDEX = 1