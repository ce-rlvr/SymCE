import sympy
from sympy import Matrix, eye, zeros, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            U = witness.get('U')
            v1 = witness.get('v1')
            v2 = witness.get('v2')
            lambda1 = witness.get('lambda1')
            lambda2 = witness.get('lambda2')
        else:
            U, v1, v2, lambda1, lambda2 = witness
            
        if isinstance(U, (list, tuple)):
            U = Matrix(U)
        if isinstance(v1, (list, tuple)):
            v1 = Matrix(v1)
        if isinstance(v2, (list, tuple)):
            v2 = Matrix(v2)
    except Exception:
        return [False, False, False, False]

    # H1: U is an n x n complex matrix, v1, v2 are n x 1 non-zero vectors
    try:
        if not isinstance(U, Matrix) or not U.is_square:
            h1 = False
        else:
            n = U.shape[0]
            if not isinstance(v1, Matrix) or v1.shape != (n, 1) or all(simplify(x) == 0 for x in v1):
                h1 = False
            elif not isinstance(v2, Matrix) or v2.shape != (n, 1) or all(simplify(x) == 0 for x in v2):
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # H2: v1 and v2 are eigenvectors of U corresponding to lambda1 and lambda2
    try:
        if h1:
            diff1 = simplify(U * v1 - lambda1 * v1)
            diff2 = simplify(U * v2 - lambda2 * v2)
            h2 = all(simplify(x) == 0 for x in diff1) and all(simplify(x) == 0 for x in diff2)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: lambda1 and lambda2 are distinct
    try:
        h3 = bool(simplify(lambda1 - lambda2) != 0)
    except Exception:
        h3 = False

    # Negated Conclusion: v1 and v2 are NOT orthogonal
    try:
        if h1:
            inner_product = simplify((v1.H * v2)[0])
            neg_q = bool(inner_product != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n matrix, v1 and v2 are non-zero n-dimensional column vectors",
    "H_2: v1 and v2 are eigenvectors of U with eigenvalues lambda1 and lambda2",
    "H_3: lambda1 and lambda2 are distinct",
    "¬Q: v1 and v2 are not orthogonal"
]

N_HYP = 3
NEG_Q_INDEX = 3