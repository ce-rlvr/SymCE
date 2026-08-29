import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a bilinear form on V",
    "H_3: A is the matrix representation of B with respect to a basis beta",
    "H_4: P is the change of basis matrix from gamma to beta",
    "¬Q: C != P^T A P"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    # Extract A, P, C from the witness
    try:
        if isinstance(witness, dict):
            A = witness['A']
            P = witness['P']
            C = witness['C']
        elif hasattr(witness, 'A') and hasattr(witness, 'P') and hasattr(witness, 'C'):
            A = witness.A
            P = witness.P
            C = witness.C
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            A = witness[-3]
            P = witness[-2]
            C = witness[-1]
        else:
            return [False] * 5

        # Convert to sympy Matrices if they are not already
        if not hasattr(A, 'shape'):
            A = Matrix(A)
        if not hasattr(P, 'shape'):
            P = Matrix(P)
        if not hasattr(C, 'shape'):
            C = Matrix(C)
    except Exception:
        return [False] * 5

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = hasattr(A, 'shape') and hasattr(P, 'shape') and hasattr(C, 'shape')
    except Exception:
        h1 = False

    # H_2: B is a bilinear form on V
    try:
        h2 = getattr(A, 'is_square', False)
    except Exception:
        h2 = False

    # H_3: A is the matrix representation of B with respect to a basis beta
    try:
        h3 = getattr(A, 'is_square', False)
    except Exception:
        h3 = False

    # H_4: P is the change of basis matrix from gamma to beta
    try:
        h4 = getattr(P, 'is_square', False) and P.shape == A.shape and P.det() != 0
    except Exception:
        h4 = False

    # ¬Q: C != P^T A P
    try:
        expected_C = P.T * A * P
        if C.shape != expected_C.shape:
            neg_q = True
        else:
            neg_q = bool(C != expected_C)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]