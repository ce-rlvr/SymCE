import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H1: A is an m x n complex matrix
    try:
        # Check if A acts like a matrix
        h1 = hasattr(A, 'singular_values') and hasattr(A, 'rows') and hasattr(A, 'cols')
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails
    try:
        # If B is not a matrix, it doesn't have singular values, so the conclusion fails.
        if not (hasattr(B, 'singular_values') and hasattr(B, 'rows') and hasattr(B, 'cols')):
            neg_q = True
        else:
            try:
                sv_B = B.singular_values()
            except Exception:
                # If B is a matrix but we cannot compute its singular values, the conclusion fails.
                neg_q = True
            else:
                sv_A = A.singular_values()
                expected = sorted([a * b for a in sv_A for b in sv_B])
                
                # Compute the Kronecker product A \otimes B
                AB = sympy.Matrix(A.rows * B.rows, A.cols * B.cols, 
                                  lambda i, j: A[i // B.rows, j // B.cols] * B[i % B.rows, j % B.cols])
                actual = sorted(AB.singular_values())
                
                match = True
                if len(expected) != len(actual):
                    match = False
                else:
                    for e, a in zip(expected, actual):
                        diff = sympy.simplify(e - a)
                        if diff != 0:
                            # Fallback to numerical evaluation to account for equivalent unsimplified expressions
                            try:
                                if abs(complex(diff.evalf())) > 1e-9:
                                    match = False
                                    break
                            except Exception:
                                match = False
                                break
                neg_q = not match
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "¬Q: The multiset of singular values of A \\otimes B does not consist of all pairwise products of singular values of A and B"
]

N_HYP = 1
NEG_Q_INDEX = 1