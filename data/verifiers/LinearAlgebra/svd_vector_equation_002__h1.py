import sympy as sp
from sympy import simplify, eye

def conditions(witness) -> list[bool]:
    # Extract variables from the witness
    if isinstance(witness, dict):
        A = witness.get('A')
        U = witness.get('U')
        Sigma = witness.get('Sigma')
        V = witness.get('V')
        i = witness.get('i')
        u_i = witness.get('u_i')
        v_i = witness.get('v_i')
        sigma_i = witness.get('sigma_i')
    else:
        try:
            # Try unpacking as an 8-tuple
            A, U, Sigma, V, u_i, v_i, sigma_i, i = witness
        except Exception:
            try:
                # Try unpacking as a 5-tuple
                A, U, Sigma, V, i = witness
                u_i, v_i, sigma_i = None, None, None
            except Exception:
                return [False, False, False, False, False]

    # H1: A = U \Sigma V^* is a singular value decomposition of A.
    h1 = False
    try:
        m, n = A.shape
        # Allow both full SVD and compact/thin SVD dimensions
        k = U.shape[1]
        if U.shape[0] == m and V.shape[0] == n and Sigma.shape == (k, V.shape[1]):
            # Check if U and V have orthonormal columns (unitary/isometry)
            U_is_iso = simplify(U.H * U - eye(k)).is_zero_matrix
            V_is_iso = simplify(V.H * V - eye(V.shape[1])).is_zero_matrix
            if U_is_iso and V_is_iso:
                # Check if Sigma is diagonal with non-negative real entries
                is_diag = True
                for r in range(Sigma.shape[0]):
                    for c in range(Sigma.shape[1]):
                        val = simplify(Sigma[r, c])
                        if r != c and val != 0:
                            is_diag = False
                        if r == c and (not val.is_real or val < 0):
                            is_diag = False
                if is_diag:
                    # Check if A = U * Sigma * V^*
                    if simplify(A - U * Sigma * V.H).is_zero_matrix:
                        h1 = True
    except Exception:
        h1 = False

    # H2: u_i is the i-th column of the matrix U.
    h2 = False
    try:
        expected_u_i = U[:, i]
        if u_i is None:
            u_i = expected_u_i
            h2 = True
        else:
            if simplify(u_i - expected_u_i).is_zero_matrix:
                h2 = True
    except Exception:
        h2 = False

    # H3: v_i is the i-th column of the matrix V.
    h3 = False
    try:
        expected_v_i = V[:, i]
        if v_i is None:
            v_i = expected_v_i
            h3 = True
        else:
            if simplify(v_i - expected_v_i).is_zero_matrix:
                h3 = True
    except Exception:
        h3 = False

    # H4: \sigma_i is the i-th diagonal element of the matrix \Sigma.
    h4 = False
    try:
        expected_sigma_i = Sigma[i, i]
        if sigma_i is None:
            sigma_i = expected_sigma_i
            h4 = True
        else:
            if simplify(sigma_i - expected_sigma_i) == 0:
                h4 = True
    except Exception:
        h4 = False

    # Conclusion: The matrix-vector product A v_i is equal to the scalar multiple \sigma_i u_i.
    # neg_Q is True if the conclusion FAILS.
    neg_q = False
    try:
        lhs = A * v_i
        rhs = sigma_i * u_i
        if not simplify(lhs - rhs).is_zero_matrix:
            neg_q = True
    except Exception:
        # If the conclusion cannot be evaluated (e.g., dimension mismatch), it fails to hold.
        neg_q = True

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: A = U \\Sigma V^* is a singular value decomposition of A",
    "H_2: u_i is the i-th column of the matrix U",
    "H_3: v_i is the i-th column of the matrix V",
    "H_4: \\sigma_i is the i-th diagonal element of the matrix \\Sigma",
    "¬Q: The matrix-vector product A v_i is NOT equal to the scalar multiple \\sigma_i u_i"
]

N_HYP = 4
NEG_Q_INDEX = 4

# Top-level setup for standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)