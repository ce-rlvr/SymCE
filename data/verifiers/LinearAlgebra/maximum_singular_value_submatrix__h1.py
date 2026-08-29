import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (A, B) of matrices (or nested lists).
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        A_orig, B_orig = witness
        A = Matrix(A_orig)
        B = Matrix(B_orig)
    except Exception:
        return [False, False]

    # H_1: B is a submatrix formed by deleting any number of rows and/or columns from A
    h1_ok = False
    try:
        m, n = A.shape
        mb, nb = B.shape
        if mb <= m and nb <= n:
            for row_indices in itertools.combinations(range(m), mb):
                for col_indices in itertools.combinations(range(n), nb):
                    sub = A.extract(list(row_indices), list(col_indices))
                    if sub == B:
                        h1_ok = True
                        break
                if h1_ok:
                    break
    except Exception:
        h1_ok = False

    # neg_Q: The maximum singular value of B is strictly greater than the maximum singular value of A
    neg_q_ok = False
    try:
        def get_max_sv(M):
            svs = M.singular_values()
            if not svs:
                return sympy.S.Zero
            try:
                # Try to find the maximum numerically first for robustness
                return max(svs, key=lambda x: float(x.evalf()))
            except Exception:
                # Fallback to symbolic Max if numerical evaluation fails
                from sympy import Max
                return Max(*svs)

        max_A = get_max_sv(A)
        max_B = get_max_sv(B)

        try:
            neg_q_ok = float(max_B.evalf()) > float(max_A.evalf())
        except Exception:
            neg_q_ok = bool(max_B > max_A)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is a submatrix formed by deleting any number of rows and/or columns from A",
    "¬Q: The maximum singular value of B is strictly greater than the maximum singular value of A"
]

N_HYP = 1
NEG_Q_INDEX = 1