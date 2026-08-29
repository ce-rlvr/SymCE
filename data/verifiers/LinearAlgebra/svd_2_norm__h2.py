import sympy
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, sigma_1 = witness
        elif isinstance(witness, dict):
            A = witness.get('A')
            sigma_1 = witness.get('sigma_1')
        else:
            A = witness
            sigma_1 = None
    except Exception:
        A = None
        sigma_1 = None

    # H_1: A is an m x n complex matrix
    try:
        h1 = isinstance(A, sympy.MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: The induced 2-norm of A is not equal to sigma_1
    try:
        if sigma_1 is None:
            neg_q = False
        else:
            norm_A = A.norm(2)
            diff = sympy.simplify(norm_A - sigma_1)
            if diff == 0:
                neg_q = False
            else:
                try:
                    # Check for numerical equivalence in case of floating point inaccuracies
                    neg_q = abs(complex(diff)) > 1e-9
                except Exception:
                    # If it cannot be evaluated to a complex number (e.g., contains symbols)
                    # and didn't simplify to 0, we consider it not equal.
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The induced 2-norm of A is not equal to sigma_1"
]

N_HYP = 1
NEG_Q_INDEX = 1