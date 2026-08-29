import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (list, tuple)):
            A = sympy.Matrix(witness)
        else:
            A = witness
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = all(sympy.sympify(e).is_complex for e in A)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            # The conclusion states that A has all real eigenvalues and is unitarily 
            # diagonalizable to a real diagonal matrix. Mathematically, this holds 
            # if and only if A is a Hermitian matrix.
            # Therefore, the conclusion fails (neg_Q is True) iff A is NOT Hermitian.
            diff = sympy.simplify(A - A.H)
            neg_q = bool(diff != sympy.zeros(*A.shape))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n square matrix",
    "H_2: The entries of A are complex numbers",
    "¬Q: A is not Hermitian (so it does not have all real eigenvalues or is not unitarily diagonalizable to a real diagonal matrix)"
]

N_HYP = 2
NEG_Q_INDEX = 2