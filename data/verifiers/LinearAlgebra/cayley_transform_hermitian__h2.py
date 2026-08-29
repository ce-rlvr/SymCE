import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
        if witness.shape[0] != witness.shape[1]:
            h1 = False
        else:
            diff_H = witness - witness.H
            h1 = all(sympy.simplify(val) == 0 for val in diff_H)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, sympy.MatrixBase):
            witness = sympy.Matrix(witness)
        if witness.shape[0] != witness.shape[1]:
            neg_q = True
        else:
            n = witness.shape[0]
            I_mat = sympy.eye(n)
            
            mat_to_invert = I_mat + sympy.I * witness
            
            if sympy.simplify(mat_to_invert.det()) == 0:
                neg_q = True
            else:
                mat_inv = mat_to_invert.inv()
                U = (I_mat - sympy.I * witness) * mat_inv
                
                diff_U = U * U.H - I_mat
                is_unitary = all(sympy.simplify(val) == 0 for val in diff_U)
                neg_q = not is_unitary
                
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is an n x n Hermitian matrix",
    "¬Q: U = (I - iH)(I + iH)^{-1} is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1