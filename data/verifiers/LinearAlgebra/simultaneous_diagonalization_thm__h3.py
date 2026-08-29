import sympy
from sympy import Matrix, eye, zeros
import itertools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: S is a set of n by n matrices over a field F
    try:
        h1 = False
        if isinstance(witness, (list, tuple, set)) and len(witness) > 0:
            h1 = True
            n = None
            for A in witness:
                if not isinstance(A, sympy.MatrixBase) or not A.is_square:
                    h1 = False
                    break
                if n is None:
                    n = A.shape[0]
                elif A.shape[0] != n:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: Every matrix in S is diagonalizable
    try:
        h2 = False
        if h1:
            h2 = all(A.is_diagonalizable() for A in witness)
    except Exception:
        h2 = False

    # ¬Q: The matrices in S are NOT simultaneously diagonalizable.
    # A set of diagonalizable matrices is simultaneously diagonalizable 
    # if and only if they commute pairwise. Thus, they fail to be 
    # simultaneously diagonalizable iff at least one pair does not commute.
    try:
        neg_q = False
        if h1:
            for A, B in itertools.combinations(witness, 2):
                diff = A * B - B * A
                is_zero = True
                for val in diff:
                    if sympy.simplify(val) != 0:
                        is_zero = False
                        break
                if not is_zero:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a set of n by n matrices",
    "H_2: Every matrix in S is diagonalizable",
    "¬Q: The matrices in S are not simultaneously diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2