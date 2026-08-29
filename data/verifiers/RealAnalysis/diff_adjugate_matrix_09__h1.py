import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    
    The conjecture claims that the adjugate matrix function is differentiable everywhere on M_n(R).
    Since the entries of the adjugate matrix are polynomials (determinants of (n-1)x(n-1) submatrices) 
    in the entries of the original matrix, the adjugate function is a polynomial mapping. 
    Polynomial mappings are infinitely differentiable everywhere on their domain.
    Therefore, the conclusion is mathematically ALWAYS TRUE, meaning its negation is ALWAYS FALSE.
    """
    # H_1: adj is the adjugate matrix function on M_n(R)
    # This is a definitional hypothesis. We verify the witness is a valid dimension n or a matrix.
    try:
        if isinstance(witness, sp.MatrixBase):
            h1_ok = True
        else:
            n = int(witness)
            h1_ok = (n >= 1)
    except Exception:
        h1_ok = False

    # ¬Q: adj is NOT differentiable everywhere on M_n(R)
    # As established, the adjugate function is everywhere differentiable.
    neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: adj is the adjugate matrix function on M_n(R)",
    "¬Q: adj is not differentiable everywhere on M_n(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1