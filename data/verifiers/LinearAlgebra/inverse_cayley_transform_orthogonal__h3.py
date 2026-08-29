import sympy
from sympy import Matrix, eye, zeros, MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(e):
    if hasattr(e, 'is_zero') and e.is_zero:
        return True
    try:
        return sympy.simplify(e) == 0
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, (list, tuple)):
            witness = Matrix(witness)
    except Exception:
        pass

    # H1: Q is an n x n real matrix
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = True
            for elem in witness:
                if elem.is_real is False or elem.has(sympy.I):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: Q is an orthogonal matrix
    try:
        if h1:
            n = witness.shape[0]
            diff = witness.T * witness - eye(n)
            h2 = all(is_zero(e) for e in diff)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: (I-Q)(I+Q)^{-1} is NOT a skew-symmetric matrix
    try:
        if h1:
            n = witness.shape[0]
            I_mat = eye(n)
            I_plus_Q = I_mat + witness
            I_minus_Q = I_mat - witness
            
            if is_zero(I_plus_Q.det()):
                neg_q = True
            else:
                M = I_minus_Q * I_plus_Q.inv()
                diff = M.T + M
                is_skew = all(is_zero(e) for e in diff)
                neg_q = not is_skew
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "H_2: Q is an orthogonal matrix",
    "¬Q: (I-Q)(I+Q)^{-1} is not a skew-symmetric matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2