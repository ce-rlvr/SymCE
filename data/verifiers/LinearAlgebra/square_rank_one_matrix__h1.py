import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: Suppose the rank of A is exactly 1
    try:
        h1 = bool(witness.rank() == 1)
    except Exception:
        h1 = False

    # Conclusion: A^2 = tr(A)A
    # If A is not square, A**2 or A.trace() will raise an exception,
    # meaning the conclusion is undefined (and thus fails to hold).
    try:
        lhs = witness ** 2
        rhs = witness.trace() * witness
        q = bool(lhs == rhs)
    except Exception:
        q = False

    neg_q = not q

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: the rank of A is exactly 1",
    "¬Q: A^2 != tr(A)A (or operation is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1