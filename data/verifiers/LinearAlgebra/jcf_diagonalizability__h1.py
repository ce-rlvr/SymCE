import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for Linear Algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a tuple (A, J), a dict {'A': A, 'J': J}, or just a matrix A.
    """
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            J = witness.get('J')
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, J = witness
        else:
            A = witness
            J = A.jordan_form()[1]
    except Exception:
        return [False, False]

    # H_1: J is the Jordan canonical form of A
    try:
        _, J_actual = A.jordan_form()
        h1 = bool(J == J_actual)
    except Exception:
        h1 = False

    # ¬Q: The conclusion FAILS at the witness.
    # The conclusion is: "A is diagonalizable if and only if every Jordan block in J is a 1x1 matrix."
    # This is false if we consider diagonalizability over the base field (e.g., R for real matrices),
    # because a real matrix might have a diagonal complex Jordan form but not be diagonalizable over R.
    try:
        # Check if A is diagonalizable over its base field.
        # If all entries are real, we check diagonalizability over the reals.
        if all(getattr(e, 'is_real', False) == True for e in A):
            a_diag = bool(A.is_diagonalizable(reals_only=True))
        else:
            a_diag = bool(A.is_diagonalizable())
            
        # Every Jordan block in J is a 1x1 matrix iff J is a diagonal matrix
        j_diag = bool(J.is_diagonal())
        
        # The conclusion fails if the two truth values are not equal
        neg_q = (a_diag != j_diag)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: J is the Jordan canonical form of A",
    "¬Q: It is not the case that A is diagonalizable if and only if every Jordan block in J is a 1x1 matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1