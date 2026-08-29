import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: A is a matrix (so that A^+ is well-defined)
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # neg_Q: A^+ is NOT positive semidefinite
    try:
        if not h1:
            neg_q = False
        else:
            A_pinv = witness.pinv()
            
            # A matrix is positive semidefinite if it is square, Hermitian, 
            # and all its eigenvalues are non-negative.
            if not A_pinv.is_square:
                is_psd = False
            else:
                is_hermitian = (A_pinv == A_pinv.H)
                if not is_hermitian:
                    is_psd = False
                else:
                    is_psd = True
                    evals = A_pinv.eigenvals()
                    for val in evals.keys():
                        if val.is_real is False:
                            is_psd = False
                            break
                        try:
                            if bool(val < 0):
                                is_psd = False
                                break
                        except TypeError:
                            # If we cannot evaluate val < 0, assume it's not PSD
                            is_psd = False
                            break
            
            neg_q = not is_psd
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a matrix",
    "¬Q: A^+ is not positive semidefinite"
]

N_HYP = 1
NEG_Q_INDEX = 1