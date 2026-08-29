import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, (list, tuple)) and len(witness) == 2):
            h1_ok = False
        else:
            A, B = witness
            A_mat = Matrix(A)
            B_mat = Matrix(B)
            h1_ok = bool(A_mat.is_square and B_mat.is_square and A_mat.shape == B_mat.shape)
    except Exception:
        h1_ok = False

    try:
        if not (isinstance(witness, (list, tuple)) and len(witness) == 2):
            neg_q_ok = False
        else:
            A, B = witness
            A_mat = Matrix(A)
            B_mat = Matrix(B)
            comm = A_mat * B_mat - B_mat * A_mat
            diff = comm.H + comm
            if diff.is_zero_matrix:
                neg_q_ok = False
            else:
                diff_simp = sympy.simplify(diff)
                if diff_simp.is_zero_matrix:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "¬Q: The commutator AB - BA is not a skew-adjoint operator"
]

N_HYP = 1
NEG_Q_INDEX = 1