import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif witness.rows != witness.cols:
            h1 = False
        elif witness.rows < 1:
            h1 = False
        else:
            h1 = all(elem.is_real == True for elem in witness)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, Matrix) or witness.rows != witness.cols or witness.rows < 1:
            neg_q = False
        else:
            n = witness.rows
            I = eye(n)
            I_plus_A = I + witness
            
            det_val = sympy.simplify(I_plus_A.det())
            if det_val == 0:
                neg_q = True
            else:
                try:
                    I_plus_A_inv = I_plus_A.inv()
                except Exception:
                    neg_q = True
                else:
                    I_minus_A = I - witness
                    Q = I_minus_A * I_plus_A_inv
                    diff = Q.T * Q - I
                    is_zero = all(sympy.simplify(val) == 0 for val in diff)
                    neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real matrix",
    "¬Q: I + A is not invertible or Q = (I - A)(I + A)^{-1} is not orthogonal"
]

N_HYP = 1
NEG_Q_INDEX = 1