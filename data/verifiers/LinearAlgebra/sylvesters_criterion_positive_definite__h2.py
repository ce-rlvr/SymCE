import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: A is a real square matrix representing a bilinear form
        if not isinstance(witness, Matrix):
            h1 = False
        elif witness.rows != witness.cols or witness.rows < 1:
            h1 = False
        else:
            h1 = True
            for i in range(witness.rows):
                for j in range(witness.cols):
                    try:
                        float(witness[i, j])
                    except Exception:
                        h1 = False
                        break
    except Exception:
        h1 = False

    try:
        # A bilinear form B is positive definite iff its symmetric part is positive definite.
        # A symmetric matrix is positive definite iff all its leading principal minors are strictly positive.
        sym_A = (witness + witness.T) / 2
        is_B_pos_def = True
        for k in range(1, sym_A.rows + 1):
            minor = sym_A[:k, :k].det()
            if float(minor) <= 0:
                is_B_pos_def = False
                break
        
        # Check if all leading principal minors of A are strictly positive
        are_A_minors_pos = True
        for k in range(1, witness.rows + 1):
            minor = witness[:k, :k].det()
            if float(minor) <= 0:
                are_A_minors_pos = False
                break
        
        # The conclusion is an equivalence (iff). Its negation is the XOR of the two sides.
        neg_q = (is_B_pos_def != are_A_minors_pos)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a real square matrix representing a bilinear form",
    "¬Q: B is positive definite XOR all leading principal minors of A are strictly positive"
]

N_HYP = 1
NEG_Q_INDEX = 1