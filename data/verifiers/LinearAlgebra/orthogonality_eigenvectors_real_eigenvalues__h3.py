import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            Q = witness.get('Q')
            lambda_1 = witness.get('lambda_1')
            lambda_2 = witness.get('lambda_2')
            v_1 = witness.get('v_1')
            v_2 = witness.get('v_2')
        else:
            Q, lambda_1, lambda_2, v_1, v_2 = witness
    except Exception:
        return [False, False, False]

    # H1: Q is an n x n real orthogonal matrix
    h1 = False
    try:
        Q_mat = Matrix(Q)
        if Q_mat.is_square:
            n = Q_mat.shape[0]
            is_real = all(sp.simplify(sp.im(Q_mat[i, j])) == 0 for i in range(n) for j in range(n))
            if is_real:
                diff = Q_mat.T * Q_mat - eye(n)
                if all(sp.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n)):
                    h1 = True
    except Exception:
        h1 = False

    # H2: lambda_1 and lambda_2 are distinct real eigenvalues of Q
    h2 = False
    try:
        Q_mat = Matrix(Q)
        l1 = sp.sympify(lambda_1)
        l2 = sp.sympify(lambda_2)
        if sp.simplify(sp.im(l1)) == 0 and sp.simplify(sp.im(l2)) == 0:
            if sp.simplify(l1 - l2) != 0:
                n = Q_mat.shape[0]
                char_poly_1 = (Q_mat - l1 * eye(n)).det()
                char_poly_2 = (Q_mat - l2 * eye(n)).det()
                if sp.simplify(char_poly_1) == 0 and sp.simplify(char_poly_2) == 0:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: v_1 and v_2 are NOT orthogonal
    neg_q = False
    try:
        v1_mat = Matrix(v_1)
        v2_mat = Matrix(v_2)
        dot_product = sp.simplify(v1_mat.dot(v2_mat))
        if dot_product != 0:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "H_2: lambda_1 and lambda_2 are distinct real eigenvalues of Q",
    "¬Q: v_1 and v_2 are not orthogonal"
]

N_HYP = 2
NEG_Q_INDEX = 2