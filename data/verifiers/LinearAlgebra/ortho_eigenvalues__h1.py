import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        Q, lam = witness
    except Exception:
        return [False, False, False]
    
    # H1: Q is an orthogonal matrix
    try:
        if not getattr(Q, 'is_Matrix', False) or Q.shape[0] != Q.shape[1]:
            h1 = False
        else:
            n = Q.shape[0]
            diff = Q.T * Q - sp.eye(n)
            h1 = all(sp.simplify(x) == 0 for x in diff)
    except Exception:
        h1 = False

    # H2: lambda is an eigenvalue of Q
    try:
        if not getattr(Q, 'is_Matrix', False) or Q.shape[0] != Q.shape[1]:
            h2 = False
        else:
            n = Q.shape[0]
            char_poly_val = (Q - lam * sp.eye(n)).det()
            h2 = sp.simplify(char_poly_val) == 0
    except Exception:
        h2 = False

    # neg_Q: The complex modulus (absolute value) of lambda is not equal to 1
    try:
        val = sp.simplify(sp.Abs(lam) - 1)
        neg_q = val != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: lambda is an eigenvalue of Q",
    "¬Q: The complex modulus (absolute value) of lambda is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2