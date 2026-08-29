import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # H_1: A is an n x n complex matrix
        h1 = hasattr(witness, 'is_square') and witness.is_square
    except Exception:
        h1 = False

    try:
        # ¬Q: The matrix exponential e^A is not a unitary matrix
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            eA = witness.exp()
            # A matrix U is unitary if U * U^H = I
            diff = sympy.simplify(eA * eA.adjoint() - eye(n))
            is_zero = diff.is_zero_matrix
            
            if is_zero is not None:
                neg_q = not is_zero
            else:
                # Fallback to numerical evaluation if symbolic simplification is inconclusive
                diff_num = diff.evalf()
                neg_q = any(abs(diff_num[i, j]) > 1e-9 for i in range(n) for j in range(n))
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The matrix exponential e^A is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1