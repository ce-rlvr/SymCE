import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = (
            isinstance(witness, Matrix) and 
            witness.rows == witness.cols and 
            witness.rows > 0 and 
            all(e.is_real for e in witness)
        )
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # The conclusion states there exists a UNIQUE QR decomposition with R having strictly positive diagonal entries.
            # This is true if and only if A is invertible.
            # If A is singular (det(A) == 0), det(R) would have to be 0, so R cannot have strictly positive diagonal entries.
            # Thus, 0 such decompositions exist, which means the existence of a unique one is FALSE.
            neg_q = bool(witness.det() == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a real n x n matrix",
    "¬Q: A does not have a unique QR decomposition with strictly positive diagonal entries in R"
]

N_HYP = 1
NEG_Q_INDEX = 1