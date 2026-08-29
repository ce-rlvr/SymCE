import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    matrix_witness = None
    
    # H_1: A is an n \times n matrix over the real numbers.
    try:
        if not isinstance(witness, Matrix):
            matrix_witness = Matrix(witness)
        else:
            matrix_witness = witness
            
        if not matrix_witness.is_square:
            h1 = False
        else:
            h1 = True
            for elem in matrix_witness:
                if sympy.im(elem) != 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: Every non-zero singular value of A has an even multiplicity (negated)
    # i.e., A has at least one non-zero singular value with an odd multiplicity.
    try:
        if not h1 or matrix_witness is None:
            neg_q = False
        else:
            # Singular values of A are the square roots of the eigenvalues of A^T A.
            # The multiplicity of a singular value is the same as the multiplicity 
            # of the corresponding eigenvalue of A^T A.
            M = matrix_witness.T * matrix_witness
            eigenvals = M.eigenvals()
            neg_q = False
            for val, mult in eigenvals.items():
                if val == 0:
                    continue
                try:
                    val_simp = sympy.simplify(val)
                    if val_simp.is_zero or val_simp == 0:
                        continue
                except Exception:
                    pass
                
                if mult % 2 != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over the real numbers",
    "¬Q: A has a non-zero singular value with an odd multiplicity"
]

N_HYP = 1
NEG_Q_INDEX = 1