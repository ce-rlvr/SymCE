import sympy
from sympy import Matrix, MatrixBase, eye, zeros, Poly
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H1: A is a square matrix of size n >= 1
    try:
        if not isinstance(witness, MatrixBase):
            A = Matrix(witness)
        else:
            A = witness
        h1 = bool(A.is_square and A.shape[0] >= 1)
    except Exception:
        h1 = False
        A = None

    # H2: Entries of A belong to a principal ideal domain
    h2 = False
    try:
        if h1 and A is not None:
            # Z is a PID
            if all(getattr(e, 'is_Integer', False) == True for e in A):
                h2 = True
            # Q is a field, hence a PID
            elif all(getattr(e, 'is_Rational', False) == True for e in A):
                h2 = True
            # F[x] is a PID
            else:
                syms = A.free_symbols
                if len(syms) == 1:
                    sym = list(syms)[0]
                    is_poly = True
                    for e in A:
                        try:
                            Poly(e, sym)
                        except Exception:
                            is_poly = False
                            break
                    h2 = is_poly
    except Exception:
        h2 = False

    # neg_Q: A is NOT similar over R to a diagonal matrix of 1s and 0s
    # Over a PID, an idempotent matrix is always diagonalizable to 1s and 0s.
    # Conversely, any matrix similar to a diagonal matrix of 1s and 0s must be idempotent.
    # Therefore, the conclusion fails if and only if A is NOT idempotent.
    neg_q = False
    try:
        if h1 and A is not None:
            neg_q = bool(A * A != A)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix of size n >= 1",
    "H_2: Entries of A belong to a principal ideal domain",
    "¬Q: A is not similar over R to a diagonal matrix whose diagonal entries are exclusively 1s and 0s"
]

N_HYP = 2
NEG_Q_INDEX = 2