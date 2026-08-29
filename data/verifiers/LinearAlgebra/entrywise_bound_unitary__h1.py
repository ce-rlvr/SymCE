import sympy as sp
from sympy import eye, zeros, I, Rational, sqrt
from sympy.matrices import MatrixBase

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    # H_1: U is a unitary matrix
    try:
        if not isinstance(witness, MatrixBase):
            U = sp.Matrix(witness)
        else:
            U = witness
            
        if not hasattr(U, 'shape') or len(U.shape) != 2:
            h1 = False
        elif U.shape[0] != U.shape[1]:
            h1 = False
        else:
            n = U.shape[0]
            prod = U * U.H
            if prod == eye(n):
                h1 = True
            elif sp.expand(prod) == eye(n):
                h1 = True
            else:
                h1 = bool(sp.simplify(prod) == eye(n))
    except Exception:
        h1 = False

    # neg_Q: Not every individual entry of U has a complex modulus less than or equal to 1
    # (i.e., there exists at least one entry with a complex modulus strictly greater than 1)
    try:
        if not isinstance(witness, MatrixBase):
            U = sp.Matrix(witness)
        else:
            U = witness
            
        neg_q = False
        for entry in U:
            if bool(sp.Abs(entry) > 1):
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: U has at least one entry with complex modulus strictly greater than 1"
]

N_HYP = 1
NEG_Q_INDEX = 1