import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: U is the ring of n by n strictly upper triangular matrices with entries in R",
    "H_3: A is a matrix in U",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_nonzero(val):
    try:
        if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix is not None:
            return not val.is_zero_matrix
        if val == 0:
            return False
        return bool(sp.simplify(val) != 0)
    except Exception:
        return True

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                n, A = witness
            elif len(witness) == 3:
                n, U, A = witness
            else:
                A = witness[-1]
                n = A.shape[0] if hasattr(A, 'shape') else len(A)
        else:
            A = witness
            n = A.shape[0] if hasattr(A, 'shape') else len(A)
            
        if not hasattr(A, 'shape'):
            A = sp.Matrix(A)
    except Exception:
        return [False, False, False, False]

    # H1: n is a positive integer
    try:
        h1 = False
        if int(n) == n and n > 0:
            h1 = True
    except Exception:
        h1 = False

    # H2: U is the ring of n by n strictly upper triangular matrices with entries in R
    try:
        h2 = hasattr(A, 'shape') and len(A.shape) == 2
    except Exception:
        h2 = False

    # H3: A is a matrix in U
    try:
        h3 = False
        if A.shape == (n, n):
            h3 = True
            for i in range(n):
                for j in range(i + 1):
                    if is_nonzero(A[i, j]):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # Neg_Q: A^n is not the zero matrix
    try:
        An = A**n
        is_zero = True
        if hasattr(An, 'is_zero_matrix') and An.is_zero_matrix is not None:
            is_zero = An.is_zero_matrix
        else:
            for i in range(n):
                for j in range(n):
                    if is_nonzero(An[i, j]):
                        is_zero = False
                        break
                if not is_zero:
                    break
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]