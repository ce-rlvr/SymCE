import sympy
import sympy.matrices
from sympy import eye, zeros
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that T is a linear operator on V (i.e., an endomorphism).
    Without it, T can be a linear map between spaces of different dimensions (a non-square matrix),
    for which generalized eigenvectors are undefined.
    """
    try:
        # Allow lists of lists to be interpreted as matrices
        if isinstance(witness, list) and all(isinstance(row, list) for row in witness):
            matrix_witness = sympy.Matrix(witness)
        else:
            matrix_witness = witness
            
        # H1: V is a finite-dimensional vector space over the complex numbers.
        # Any matrix represents a linear map from C^n to C^m, so its domain V=C^n 
        # is a finite-dimensional vector space over C.
        h1 = isinstance(matrix_witness, sympy.matrices.MatrixBase)
    except Exception:
        h1 = False
        matrix_witness = witness

    try:
        if h1:
            # ¬Q: There does NOT exist a basis of V consisting entirely of generalized eigenvectors of T.
            # Over the complex numbers, every square matrix (endomorphism) has a basis of generalized eigenvectors.
            # The conclusion fails exactly when T is not an endomorphism (i.e., the matrix is not square),
            # because generalized eigenvectors are not defined for non-square matrices.
            neg_q = not matrix_witness.is_square
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over the complex numbers",
    "¬Q: There does not exist a basis of V consisting entirely of generalized eigenvectors of T"
]

N_HYP = 1
NEG_Q_INDEX = 1