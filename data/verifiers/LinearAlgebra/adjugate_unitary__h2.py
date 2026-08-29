import sympy
from sympy import simplify, eye, zeros, Matrix
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, MatrixBase):
            witness_mat = Matrix(witness)
        else:
            witness_mat = witness
        h1 = witness_mat.is_square
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, MatrixBase):
            witness_mat = Matrix(witness)
        else:
            witness_mat = witness
            
        adj = witness_mat.adjugate()
        det = witness_mat.det()
        conj_trans = witness_mat.H
        
        diff = adj - det * conj_trans
        is_eq = True
        for e in diff:
            if e.is_zero:
                continue
            if simplify(e) == 0:
                continue
            is_eq = False
            break
        neg_q = not is_eq
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: The adjugate matrix of U is not equal to the determinant of U multiplied by the conjugate transpose of U"
]

N_HYP = 1
NEG_Q_INDEX = 1