import sympy
from sympy import MatrixBase, eye, expand, simplify, zeros
from sympy.matrices import Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            Q = witness.get('Q')
            x = witness.get('x')
            if Q is None or x is None:
                return [False, False]
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            Q, x = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: Q is an n x n real orthogonal matrix
    try:
        h1 = False
        if isinstance(Q, MatrixBase) and Q.is_square:
            if all(e.is_real is not False for e in Q):
                I_mat = eye(Q.rows)
                diff = Q.T * Q - I_mat
                if diff.is_zero_matrix:
                    h1 = True
                else:
                    diff = expand(diff)
                    if diff.is_zero_matrix:
                        h1 = True
                    else:
                        diff = simplify(diff)
                        if diff.is_zero_matrix:
                            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The Euclidean norm ||Qx|| is not equal to the Euclidean norm ||x||
    try:
        Qx = Q * x
        norm_Qx = Qx.norm()
        norm_x = x.norm()
        if norm_Qx == norm_x:
            concl = True
        else:
            diff = simplify(norm_Qx - norm_x)
            concl = (diff == 0)
    except Exception:
        # If Q*x is undefined (e.g. dimension mismatch) or norm() fails,
        # the conclusion that they are equal is False.
        concl = False

    neg_q = not concl

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "¬Q: The Euclidean norm ||Qx|| is not equal to the Euclidean norm ||x||"
]

N_HYP = 1
NEG_Q_INDEX = 1