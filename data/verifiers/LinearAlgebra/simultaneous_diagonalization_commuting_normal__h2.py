import sympy
from sympy import Matrix, eye, zeros, expand

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple or list of two sympy.Matrix objects (S, T).
    """
    try:
        if len(witness) != 2:
            return [False, False, False]
        S, T = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional complex inner product space
    # We verify this by checking that S and T are square matrices of the same dimension >= 1.
    try:
        h1 = False
        if hasattr(S, 'shape') and hasattr(T, 'shape'):
            if S.shape == T.shape and S.shape[0] == S.shape[1] and S.shape[0] > 0:
                h1 = True
    except Exception:
        h1 = False

    def is_zero_mat(M):
        for e in M:
            if e != 0:
                try:
                    if expand(e) != 0:
                        return False
                except Exception:
                    return False
        return True

    # H_2: S and T commute, meaning ST = TS
    try:
        h2 = is_zero_mat(S * T - T * S)
    except Exception:
        h2 = False

    # ¬Q: There does NOT exist an orthonormal basis of V consisting entirely of vectors 
    # that are simultaneous eigenvectors of both S and T.
    # Two matrices have an orthonormal basis of simultaneous eigenvectors if and only if 
    # they are both normal matrices AND they commute.
    try:
        S_normal = is_zero_mat(S * S.H - S.H * S)
        T_normal = is_zero_mat(T * T.H - T.H * T)
        commute = is_zero_mat(S * T - T * S)
        neg_q = not (S_normal and T_normal and commute)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional complex inner product space",
    "H_2: S and T commute, meaning ST = TS",
    "¬Q: There does not exist an orthonormal basis of V consisting entirely of vectors that are simultaneous eigenvectors of both S and T"
]

N_HYP = 2
NEG_Q_INDEX = 2