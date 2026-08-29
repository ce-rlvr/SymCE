import math
from sympy import Matrix, eye, zeros, Rational

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: B is an n x n real positive definite matrix
    try:
        A_raw, B_raw = witness
        A = Matrix(A_raw)
        B = Matrix(B_raw)
        
        if A.shape != B.shape or A.shape[0] != A.shape[1]:
            h1_ok = False
        else:
            n = A.shape[0]
            
            def is_real_num(val):
                try:
                    float(val)
                    return True
                except Exception:
                    return False

            if not all(is_real_num(x) for x in A) or not all(is_real_num(x) for x in B):
                h1_ok = False
            elif n == 0:
                h1_ok = False
            elif B != B.T:
                h1_ok = False
            else:
                is_pd = True
                for i in range(1, n + 1):
                    if float(B[:i, :i].det()) <= 0:
                        is_pd = False
                        break
                h1_ok = is_pd
    except Exception:
        h1_ok = False

    # neg_Q: \det(A + B)^{1/n} < \det(A)^{1/n} + \det(B)^{1/n}
    try:
        A_raw, B_raw = witness
        A = Matrix(A_raw)
        B = Matrix(B_raw)
        n = A.shape[0]
        
        if n == 0:
            neg_q_ok = False
        else:
            det_A = float(A.det())
            det_B = float(B.det())
            det_AB = float((A + B).det())

            def nth_root(x, degree):
                if x < 0:
                    if degree % 2 == 0:
                        raise ValueError("Even root of negative number")
                    return -math.pow(-x, 1.0 / degree)
                return math.pow(x, 1.0 / degree)

            root_A = nth_root(det_A, n)
            root_B = nth_root(det_B, n)
            root_AB = nth_root(det_AB, n)

            neg_q_ok = root_AB < root_A + root_B - 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is an n x n real positive definite matrix",
    "¬Q: det(A + B)^{1/n} < det(A)^{1/n} + det(B)^{1/n}"
]

N_HYP = 1
NEG_Q_INDEX = 1