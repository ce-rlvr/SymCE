import sympy
from sympy import eye, zeros, im, simplify, expand
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: P is a square matrix
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: P^2 = P
    try:
        if h1:
            diff2 = witness**2 - witness
            h2 = all(expand(e) == 0 or simplify(e) == 0 for e in diff2)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: P^T = P
    try:
        if h1:
            diff3 = witness.T - witness
            h3 = all(expand(e) == 0 or simplify(e) == 0 for e in diff3)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: I - 2P is NOT an orthogonal matrix
    # An orthogonal matrix must satisfy M^T M = I AND have strictly real entries.
    try:
        if h1:
            n = witness.shape[0]
            I = eye(n)
            M = I - 2 * witness
            
            # Condition 1: M^T M == I
            diff_ortho = M.T * M - I
            is_ortho_eq = all(expand(e) == 0 or simplify(e) == 0 for e in diff_ortho)
            
            # Condition 2: M is a real matrix
            is_real = all(expand(im(e)) == 0 or simplify(im(e)) == 0 for e in M)
            
            is_ortho = is_ortho_eq and is_real
            neg_q = not is_ortho
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a square matrix",
    "H_2: P^2 = P",
    "H_3: P^T = P",
    "¬Q: I - 2P is not an orthogonal matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3