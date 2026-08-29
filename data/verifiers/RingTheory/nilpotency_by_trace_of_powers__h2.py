import sympy as sp
from sympy import Matrix, eye, zeros, Rational, Integer, Symbol

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: The trace of A^k is zero for all integers k such that 1 <= k <= n",
    "¬Q: A is not a nilpotent matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (A, n), where A is a square matrix and n is an integer.
    If only a matrix A is provided, n defaults to the dimension of A.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, n = witness
        else:
            A = witness
            n = A.shape[0]
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field of characteristic zero
    try:
        if not (isinstance(A, sp.MatrixBase) and A.is_square):
            h1_ok = False
        else:
            # In SymPy, standard matrices over Reals/Rationals/Complex are characteristic zero.
            # We ensure there are no modulo arithmetic elements (which would imply finite characteristic).
            h1_ok = not A.has(sp.Mod)
    except Exception:
        h1_ok = False

    # H_2: The trace of A^k is zero for all integers k such that 1 <= k <= n
    try:
        h2_ok = True
        for k in range(1, int(n) + 1):
            if sp.expand(sp.trace(A**k)) != 0:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # ¬Q: A is not a nilpotent matrix
    # A square matrix of size m is nilpotent iff A^m is the zero matrix.
    try:
        m = A.shape[0]
        Am = A**m
        neg_q_ok = not all(sp.expand(e) == 0 for e in Am)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]