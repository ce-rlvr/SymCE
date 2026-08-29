import sympy
from sympy import Matrix, simplify, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    A = None
    l1 = l2 = v1 = v2 = None
    
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            l1 = witness.get('lambda_1')
            l2 = witness.get('lambda_2')
            v1 = witness.get('v_1')
            v2 = witness.get('v_2')
        elif isinstance(witness, (list, tuple)) and len(witness) == 5:
            A, l1, l2, v1, v2 = witness
        else:
            A = witness
    except Exception:
        pass

    try:
        if A is not None and not isinstance(A, Matrix):
            A = Matrix(A)
        if v1 is not None and not isinstance(v1, Matrix):
            v1 = Matrix(v1)
        if v2 is not None and not isinstance(v2, Matrix):
            v2 = Matrix(v2)
            
        if v1 is not None and v1.shape[0] == 1 and v1.shape[1] > 1:
            v1 = v1.T
        if v2 is not None and v2.shape[0] == 1 and v2.shape[1] > 1:
            v2 = v2.T
    except Exception:
        pass

    if A is not None and (l1 is None or l2 is None or v1 is None or v2 is None):
        try:
            if isinstance(A, Matrix):
                eigenvects = A.eigenvects()
                if len(eigenvects) >= 2:
                    l1 = eigenvects[0][0]
                    v1 = eigenvects[0][2][0]
                    l2 = eigenvects[1][0]
                    v2 = eigenvects[1][2][0]
        except Exception:
            pass

    # H1: lambda_1 and lambda_2 are distinct
    try:
        h1 = bool(l1 != l2 and l1 is not None and l2 is not None)
    except Exception:
        h1 = False

    # H2: v_1 is a non-zero eigenvector corresponding to lambda_1
    try:
        if v1 is None or A is None or l1 is None:
            h2 = False
        else:
            diff1 = A * v1 - l1 * v1
            is_diff_zero = all(simplify(x) == 0 for x in diff1)
            is_v1_nonzero = any(simplify(x) != 0 for x in v1)
            h2 = bool(is_v1_nonzero and is_diff_zero)
    except Exception:
        h2 = False

    # H3: v_2 is a non-zero eigenvector corresponding to lambda_2
    try:
        if v2 is None or A is None or l2 is None:
            h3 = False
        else:
            diff2 = A * v2 - l2 * v2
            is_diff_zero = all(simplify(x) == 0 for x in diff2)
            is_v2_nonzero = any(simplify(x) != 0 for x in v2)
            h3 = bool(is_v2_nonzero and is_diff_zero)
    except Exception:
        h3 = False

    # neg_Q: v_1 and v_2 are NOT orthogonal (v_1^T v_2 != 0)
    try:
        if v1 is None or v2 is None:
            neg_q = False
        else:
            dot_prod = simplify((v1.T * v2)[0, 0])
            neg_q = bool(dot_prod != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: lambda_1 and lambda_2 are distinct eigenvalues",
    "H_2: v_1 is a non-zero eigenvector corresponding to lambda_1",
    "H_3: v_2 is a non-zero eigenvector corresponding to lambda_2",
    "¬Q: v_1 and v_2 are not orthogonal (v_1^T v_2 != 0)"
]

N_HYP = 3
NEG_Q_INDEX = 3