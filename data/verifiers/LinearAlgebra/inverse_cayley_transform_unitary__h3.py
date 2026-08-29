import sympy
from sympy import eye, zeros, simplify, I, expand, Matrix
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.rows == witness.cols
    except Exception:
        h1 = False

    try:
        if h1:
            n = witness.rows
            diff = expand(witness * witness.H - eye(n))
            h2 = diff == zeros(n)
            if not h2:
                diff = simplify(diff)
                h2 = diff == zeros(n)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            n = witness.rows
            I_mat = eye(n)
            denom = I_mat + witness
            det_val = simplify(denom.det())
            if det_val == 0:
                neg_q = True
            else:
                try:
                    H_mat = I * (I_mat - witness) * denom.inv()
                    diff = expand(H_mat - H_mat.H)
                    is_herm = diff == zeros(n)
                    if not is_herm:
                        diff = simplify(diff)
                        is_herm = diff == zeros(n)
                    neg_q = not is_herm
                except Exception:
                    neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "H_2: U is a unitary matrix",
    "¬Q: H = i(I - U)(I + U)^{-1} is not a Hermitian matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2