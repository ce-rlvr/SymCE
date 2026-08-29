import sympy as sp
from sympy import MatrixBase, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The expected witness is a tuple of two sympy matrices (A, B) representing 
    linear operators on a vector space V.
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                A, B = witness
            elif len(witness) == 3:
                K, A, B = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: K is an algebraically closed field
    # We evaluate the matrices over the complex numbers (or algebraic closure), 
    # so this hypothesis is considered satisfied for any valid matrix inputs.
    h1 = True

    # H2: A and B are linear operators on V
    try:
        h2 = (isinstance(A, MatrixBase) and isinstance(B, MatrixBase) and 
              A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h2 = False

    # H3: A and B commute, meaning AB = BA
    try:
        h3 = False
        if h2:
            h3 = bool(A * B == B * A)
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist a non-zero vector v in V that is an eigenvector for both A and B.
    neg_q = False
    try:
        if h2:
            n = A.shape[0]
            if n == 0:
                # For a 0-dimensional vector space, there are no non-zero vectors at all,
                # so they cannot share a non-zero eigenvector.
                neg_q = True
            else:
                shared = False
                try:
                    evals_A = A.eigenvals().keys()
                    evals_B = B.eigenvals().keys()
                    
                    for la in evals_A:
                        for lb in evals_B:
                            M1 = A - la * eye(n)
                            M2 = B - lb * eye(n)
                            # The intersection of eigenspaces is the nullspace of the stacked matrix
                            M = M1.col_join(M2)
                            if len(M.nullspace()) > 0:
                                shared = True
                                break
                        if shared:
                            break
                    neg_q = not shared
                except Exception:
                    # Fallback: Over an algebraically closed field, commuting operators 
                    # on a non-zero finite-dimensional space always share an eigenvector.
                    if h3:
                        neg_q = False
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: A and B are linear operators on V",
    "H_3: A and B commute",
    "¬Q: A and B do not share a non-zero eigenvector"
]

N_HYP = 3
NEG_Q_INDEX = 3