import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A and B are matrices in the general linear group GL_n(F)",
    "H_3: A and B each have n distinct eigenvalues in F",
    "H_4: A and B have the exact same set of eigenvalues",
    "¬Q: A and B are not conjugate in GL_n(F)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        F, A, B = witness
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        A, B = witness
        F = None
    else:
        A, B = None, None
        F = None

    # H_1: F is a field
    try:
        if F is not None and hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        else:
            # If F is not explicitly provided, we assume the matrices are over a field (e.g., QQ or CC)
            h1 = (hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix') and A.is_Matrix and B.is_Matrix)
    except Exception:
        h1 = False

    # H_2: A and B are matrices in the general linear group GL_n(F)
    try:
        h2 = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix') and A.is_Matrix and B.is_Matrix:
            if A.shape == B.shape and A.shape[0] == A.shape[1]:
                if A.det() != 0 and B.det() != 0:
                    h2 = True
    except Exception:
        h2 = False

    # H_3: A and B each have n distinct eigenvalues in F
    try:
        h3 = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix') and A.is_Matrix and B.is_Matrix:
            if A.shape == B.shape and A.shape[0] == A.shape[1]:
                n = A.shape[0]
                evals_A = A.eigenvals()
                evals_B = B.eigenvals()
                # eigenvals() returns a dict of {eigenvalue: algebraic_multiplicity}
                if len(evals_A) == n and len(evals_B) == n:
                    h3 = True
    except Exception:
        h3 = False

    # H_4: A and B have the exact same set of eigenvalues
    try:
        h4 = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix') and A.is_Matrix and B.is_Matrix:
            if A.shape == B.shape and A.shape[0] == A.shape[1]:
                set_A = set(A.eigenvals().keys())
                set_B = set(B.eigenvals().keys())
                if set_A == set_B:
                    h4 = True
    except Exception:
        h4 = False

    # ¬Q: A and B are not conjugate in GL_n(F)
    try:
        neg_q = False
        if hasattr(A, 'is_Matrix') and hasattr(B, 'is_Matrix') and A.is_Matrix and B.is_Matrix:
            if A.shape == B.shape and A.shape[0] == A.shape[1]:
                # is_similar checks if two matrices are conjugate (similar) over their field
                neg_q = not A.is_similar(B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]