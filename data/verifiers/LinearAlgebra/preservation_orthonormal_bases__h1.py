import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            S = witness.get('S')
            Q = witness.get('Q')
        else:
            S, Q = witness
        if isinstance(S, set):
            S = list(S)
    except Exception:
        return [False, False]

    # H1: S forms an orthonormal basis for R^n
    h1_ok = False
    try:
        if isinstance(S, (list, tuple)) and len(S) > 0:
            n = len(S)
            valid_S = True
            for v in S:
                if not isinstance(v, Matrix) or v.shape != (n, 1):
                    valid_S = False
                    break
            if valid_S:
                orthonormal = True
                for i in range(n):
                    for j in range(n):
                        dot_prod = S[i].dot(S[j])
                        expected = 1 if i == j else 0
                        if sympy.simplify(dot_prod - expected) != 0:
                            orthonormal = False
                            break
                    if not orthonormal:
                        break
                h1_ok = orthonormal
    except Exception:
        h1_ok = False

    # neg_Q: {Qv_1, ..., Qv_n} does NOT form an orthonormal basis for R^n
    neg_q_ok = False
    try:
        if isinstance(S, (list, tuple)) and len(S) > 0:
            n = len(S)
            if not isinstance(Q, Matrix) or Q.shape != (n, n):
                neg_q_ok = True
            else:
                QS = [Q * v for v in S]
                orthonormal = True
                for i in range(n):
                    for j in range(n):
                        dot_prod = QS[i].dot(QS[j])
                        expected = 1 if i == j else 0
                        if sympy.simplify(dot_prod - expected) != 0:
                            orthonormal = False
                            break
                    if not orthonormal:
                        break
                neg_q_ok = not orthonormal
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: S forms an orthonormal basis for R^n",
    "¬Q: {Qv_1, ..., Qv_n} does not form an orthonormal basis for R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1