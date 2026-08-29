import sympy
from sympy import Matrix, eye, zeros, I
from sympy.matrices.matrixbase import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    # H_1: A is a skew-Hermitian matrix
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            diff = witness + witness.H
            if diff.has(sympy.Symbol):
                diff = sympy.simplify(diff)
            h1 = (diff == zeros(*diff.shape))
    except Exception:
        h1 = False

    # ¬Q: A is NOT diagonalizable over the complex numbers
    try:
        if not isinstance(witness, MatrixBase):
            neg_q = False
        elif not witness.is_square:
            neg_q = False
        else:
            diag = witness.is_diagonalizable()
            if diag is False:
                neg_q = True
            elif diag is True:
                neg_q = False
            else:
                # Fallback: check if algebraic multiplicity equals geometric multiplicity for all eigenvalues
                eigenvects = witness.eigenvects()
                is_diag = True
                for evalue, alg_mult, evects in eigenvects:
                    if alg_mult != len(evects):
                        is_diag = False
                        break
                neg_q = not is_diag
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a skew-Hermitian matrix",
    "¬Q: A is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1