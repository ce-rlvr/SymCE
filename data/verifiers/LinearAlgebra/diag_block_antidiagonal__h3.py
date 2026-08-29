import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'B' not in witness:
                return [False, False, False]
            B = witness['B']
            M = witness.get('M', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[1], 'shape') and witness[1].shape[0] == 2 * witness[0].shape[0]:
                B, M = witness
            else:
                A, B = witness
                M = None
        else:
            B = witness
            M = None

        if not hasattr(B, 'shape') or B.shape[0] != B.shape[1]:
            return [False, False, False]
            
        n = B.shape[0]
    except Exception:
        return [False, False, False]

    # H1: F is a field of characteristic not equal to 2
    # Standard SymPy matrices are over fields of characteristic 0 (e.g., QQ or CC).
    h1 = True

    # H2: B is an n \times n diagonalizable matrix over F
    try:
        diag_B = B.is_diagonalizable()
        h2 = True if diag_B is True else False
    except Exception:
        h2 = False

    # neg_Q: The block matrix M is NOT diagonalizable over F
    try:
        if M is None:
            if isinstance(witness, dict) and 'A' in witness:
                A = witness['A']
            elif isinstance(witness, tuple) and len(witness) == 2 and not (hasattr(witness[1], 'shape') and witness[1].shape[0] == 2 * witness[0].shape[0]):
                A = witness[0]
            else:
                A = eye(n)
            O = zeros(n)
            # Construct block anti-diagonal matrix M = [[0, A], [B, 0]]
            M = Matrix.vstack(Matrix.hstack(O, A), Matrix.hstack(B, O))
            
        diag_M = M.is_diagonalizable()
        neg_q = True if diag_M is False else False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: B is an n x n diagonalizable matrix over F",
    "¬Q: The block matrix M is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2