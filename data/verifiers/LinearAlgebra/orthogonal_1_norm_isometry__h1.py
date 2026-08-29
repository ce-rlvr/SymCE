import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero(expr):
    """Helper to robustly check if a sympy expression is zero."""
    if expr == 0:
        return True
    try:
        n_expr = sp.N(expr)
        if n_expr.is_real:
            return abs(float(n_expr)) < 1e-9
        elif n_expr.is_complex:
            return abs(complex(n_expr)) < 1e-9
    except Exception:
        pass
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: ||Qx||_1 = ||x||_1 for all x in R^n
    # A matrix Q is a 1-norm isometry if and only if:
    # 1. The 1-norm of every column is exactly 1.
    # 2. The columns have mutually disjoint supports.
    try:
        if not isinstance(witness, sp.MatrixBase):
            h1 = False
        else:
            m, n = witness.shape
            h1 = True
            # Check column sums of absolute values
            for j in range(n):
                col_sum = sum(sp.Abs(witness[i, j]) for i in range(m))
                if not is_zero(col_sum - 1):
                    h1 = False
                    break
            # Check disjoint supports for columns
            if h1:
                for j in range(n):
                    for k in range(j + 1, n):
                        overlap = sum(sp.Abs(witness[i, j] * witness[i, k]) for i in range(m))
                        if not is_zero(overlap):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # ¬Q: Q is not a signed permutation matrix
    # A signed permutation matrix is a square matrix where each row and column
    # has exactly one non-zero entry, and that entry is 1 or -1.
    try:
        if not isinstance(witness, sp.MatrixBase):
            q_ok = False
        else:
            m, n = witness.shape
            if m != n:
                q_ok = False
            else:
                q_ok = True
                # Check rows
                for i in range(m):
                    row_nonzeros = [j for j in range(n) if not is_zero(witness[i, j])]
                    if len(row_nonzeros) != 1:
                        q_ok = False
                        break
                    if not is_zero(sp.Abs(witness[i, row_nonzeros[0]]) - 1):
                        q_ok = False
                        break
                # Check columns
                if q_ok:
                    for j in range(n):
                        col_nonzeros = [i for i in range(m) if not is_zero(witness[i, j])]
                        if len(col_nonzeros) != 1:
                            q_ok = False
                            break
                        if not is_zero(sp.Abs(witness[col_nonzeros[0], j]) - 1):
                            q_ok = False
                            break
    except Exception:
        q_ok = False

    return [h1, not q_ok]

CONDITION_LABELS = [
    "H_1: ||Qx||_1 = ||x||_1 for all x in R^n",
    "¬Q: Q is not a signed permutation matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1