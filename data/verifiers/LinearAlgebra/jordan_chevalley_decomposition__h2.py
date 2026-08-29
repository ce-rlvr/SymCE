import sympy
from sympy import Matrix, eye, zeros

# Standard linear algebra objects that might be used as witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The dropped hypothesis is that T is a linear operator on V (i.e., a square matrix).
    """
    try:
        # H_1: V is a finite-dimensional vector space over an algebraically closed field F.
        # We interpret the witness as a matrix T representing a linear map from V.
        # The domain V is finite-dimensional (number of columns), and we can assume the field is C.
        h1 = hasattr(witness, 'shape') and len(witness.shape) == 2
    except Exception:
        h1 = False

    try:
        if h1:
            # ¬Q: The conclusion fails.
            # The conclusion states T = D + N where D and N are linear operators on V.
            # This is only possible if T itself is a linear operator on V (a square matrix).
            # If T is square, the Jordan-Chevalley decomposition always exists and is unique over C.
            # If T is not square, it cannot be decomposed into operators on V.
            neg_q = witness.shape[0] != witness.shape[1]
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over an algebraically closed field F",
    "¬Q: There do not exist unique linear operators D and N on V such that T = D + N, D is diagonalizable, N is nilpotent, and DN = ND"
]

N_HYP = 1
NEG_Q_INDEX = 1