import sympy
from sympy import MatrixBase, diag, Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is an m1 x n1 complex matrix",
    "H_2: M is the (m1+m2) x (n1+n2) block diagonal matrix with diagonal blocks A and B",
    "¬Q: The multiset of singular values of M is NOT exactly the union of the multisets of singular values of A and B"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        A, B, M = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an m1 x n1 complex matrix
    try:
        h1 = isinstance(A, MatrixBase)
        if h1:
            # Check if all elements are complex numbers/expressions.
            # In sympy, numbers and most standard symbols have is_complex=True or None.
            # We only reject if it is explicitly False (e.g., infinity).
            h1 = all(getattr(e, 'is_complex', True) is not False for e in A)
    except Exception:
        h1 = False

    # H_2: M is the (m1+m2) x (n1+n2) block diagonal matrix with diagonal blocks A and B
    try:
        h2 = isinstance(B, MatrixBase) and isinstance(M, MatrixBase)
        if h2:
            expected_M = diag(A, B)
            h2 = (M.shape == expected_M.shape) and (M == expected_M)
    except Exception:
        h2 = False

    # ¬Q: The multiset of singular values of M is NOT exactly the union of the multisets of singular values of A and B
    try:
        sv_A = A.singular_values()
        sv_B = B.singular_values()
        sv_M = M.singular_values()
        
        sv_union = sv_A + sv_B
        
        if len(sv_union) != len(sv_M):
            q = False
        else:
            # Evaluate to float for robust multiset comparison
            l1 = sorted([float(abs(val.evalf())) for val in sv_union])
            l2 = sorted([float(abs(val.evalf())) for val in sv_M])
            q = all(abs(a - b) < 1e-7 for a, b in zip(l1, l2))
    except Exception:
        # If singular values cannot be computed or compared, the conclusion fails to hold.
        q = False

    neg_q = not q

    return [h1, h2, neg_q]